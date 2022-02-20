import logging
from urllib.parse import urljoin

from django import template
from django.conf import settings
from django.db.models.fields.files import ImageFieldFile
from django.templatetags.static import static
from django.utils.translation import get_language

from .models import SEOPath

logger = logging.getLogger(__name__)
register = template.Library()


def _get_meta_tags_from_context(context, path):
    flat_context = context.flatten()
    for obj in flat_context.values():
        if hasattr(obj, "get_absolute_url") and obj.get_absolute_url() == path:
            return obj, getattr(obj, "meta_tags", {})
    return (None, {})


def _get_meta_tags_for_path(path):
    return getattr(SEOPath.objects.filter(path=path).first(), "meta_tags", {})


def _override_tags(base_tags, overriding_tags):
    output = []
    for base_tag in base_tags:
        for overriding_tag in overriding_tags:
            if base_tag.get("name") == overriding_tag.get("name") and base_tag.get(
                "property"
            ) == overriding_tag.get("property"):
                output.append(overriding_tag)
                overriding_tags.remove(overriding_tag)
                break
        else:
            output.append(base_tag)
    output.extend(overriding_tags)
    return output


def _collate_meta_tags(meta_tags, default_tags):
    collated_tags = default_tags
    for language, tags in meta_tags.items():
        # Simple case, if the language isn't in the tags, dump them all in.
        if language not in collated_tags:
            collated_tags[language] = tags
            continue
        collated_tags[language] = _override_tags(
            collated_tags[language], meta_tags[language]
        )
    return collated_tags


def _get_meta_tags_for_language(meta_tags):
    if not settings.USE_I18N:
        return meta_tags.get("default", [])

    language = get_language()
    if "_" in language:
        language_tag = language[:2]
        specific_language_meta_tags = meta_tags.get(language, [])
        general_language_meta_tags = meta_tags.get(language_tag, [])
        all_language_meta_tags = _override_tags(
            general_language_meta_tags, specific_language_meta_tags
        )
    else:
        all_language_meta_tags = meta_tags.get(language, [])
    return _override_tags(meta_tags.get("default", []), all_language_meta_tags)


def _get_image_dimensions(obj, field_file):
    field = field_file.field
    if field.width_field:
        width = getattr(obj, field.width_field, field_file.width)
    else:
        width = field_file.width

    if field.height_field:
        height = getattr(obj, field.height_field, field_file.height)
    else:
        height = field_file.height
    return (width, height)


def _get_absolute_file_url(request, path):
    # Both Open Graph and Twitter Cards require absolute URLs.
    # Some static / media storages will give us absolute URLs.
    # However, the ones in Django, whitenoise, etc. just give relative URLs.
    # `urljoin()` will leave alone already-absolute URLs,
    # but we prefix relative URLs with the current site root.
    # If the sites framework is installed it uses the current site,
    # otherwise it will use data from the request object.
    # This should work for almost all cases.
    return urljoin(request.build_absolute_uri(), path)


def _parse_meta_tags(tags, request, obj):
    parsed_tags = []
    for tag in tags:
        if "content" in tag:
            parsed_tags.append(tag)
        elif "attribute" in tag:
            if not obj:
                logger.error(
                    "Trying to use `attribute` without an object for tag with name: %s",
                    tag.get("name", tag.get("property")),
                )
                continue
            attr = getattr(obj, tag["attribute"])
            if isinstance(attr, ImageFieldFile):
                field = attr
                tag["content"] = _get_absolute_file_url(request, field.url)
                parsed_tags.append(tag)
                if tag.get("property", "") in {"og:image", "og:image:url"}:
                    width, height = _get_image_dimensions(obj, field)
                    parsed_tags.append({"property": "og:image:width", "content": width})
                    parsed_tags.append(
                        {"property": "og:image:height", "content": height}
                    )
            else:
                tag["content"] = attr
                parsed_tags.append(tag)
        elif "static" in tag:
            tag["content"] = _get_absolute_file_url(request, static(tag["static"]))
            parsed_tags.append(tag)
        else:
            logger.error(
                "Missing content field for tag with name: %s",
                tag.get("name", tag.get("property")),
            )
    return parsed_tags


def get_meta_tags(context, obj=None):
    """Fetch meta tags.

    1. If an object is passed, use it.
    2. If not, try to find the object in the context.
    3. If there isn't one, check if there is an object for the current path.
    4. Grab the defaults and merge in the tags from the model.
    5. Merge in tags from the object.
    6. Get tags based on the language.
    7. Return the tags.

    The priority works like this:
    - More specific languages beat less specific ones, e.g. en_GB > en > default.
    - Tags from the object beat tags from the settings.
    """
    try:
        if obj is not None:
            found_tags = obj.meta_tags
        else:
            request_path = context["request"].path
            obj, found_tags = _get_meta_tags_from_context(context, request_path)
            if not found_tags:
                found_tags = _get_meta_tags_for_path(request_path)

        default_tags = getattr(settings, "SNAKEOIL_DEFAULT_TAGS", {})
        model_tags = getattr(obj, "snakeoil_metadata", None) or {}
        collated_tags = _collate_meta_tags(model_tags, default_tags)
        collated_tags = _collate_meta_tags(found_tags, collated_tags)
        collated_tags = _get_meta_tags_for_language(collated_tags)
        meta_tags = _parse_meta_tags(collated_tags, request=context["request"], obj=obj)
        return {"meta_tags": meta_tags}
    except Exception:
        logger.exception("Failed fetching meta tags")
        return {"meta_tags": []}
