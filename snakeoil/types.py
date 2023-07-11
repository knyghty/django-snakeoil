import typing

MetaTagKey = typing.Literal["attribute", "content", "name", "property", "static"]
MetaTag = typing.Dict[MetaTagKey, str]
MetaTagList = typing.List[MetaTag]
MetaTagLanguageList = typing.Dict[str, MetaTagList]
MetaTagContext = typing.Dict[typing.Literal["meta_tags"], MetaTagList]
