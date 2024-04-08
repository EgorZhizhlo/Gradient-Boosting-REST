from marshmallow import Schema, fields


class modelS(Schema):
    id = fields.Int()
    totsp = fields.Str()
    dist = fields.Str()
    metrdist = fields.Str()
    walk = fields.Str()
    price = fields.Str()
    pred = fields.Str()
    error = fields.Str()
