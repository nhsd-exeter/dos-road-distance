from common import Common
from main import RoadDistance

common = Common()
rd = RoadDistance({})

tmp_local = rd.contracts["local"]
rd.contracts["local"] = "some_unknown_contract"

rd.validate_against_schema({}, "local")

rd.contracts["local"] = tmp_local
