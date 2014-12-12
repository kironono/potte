# coding: utf-8

import colander
import deform


class PhotoUploadSchema(colander.Schema):
    uuid = colander.SchemaNode(
        colander.String(),
        required=True,
    )
    file = colander.SchemaNode(
        deform.FileData(),
        required=True,
    )
