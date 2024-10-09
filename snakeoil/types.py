import typing

MetaTagKey = typing.Literal["attribute", "content", "name", "property", "static"]
MetaTag = dict[MetaTagKey, str]
MetaTagList = list[MetaTag]
MetaTagLanguageList = dict[str, MetaTagList]
MetaTagContext = dict[typing.Literal["meta_tags"], MetaTagList]
