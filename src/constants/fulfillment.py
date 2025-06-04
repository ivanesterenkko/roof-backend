from enum import StrEnum


class FulfillmentStatus(StrEnum):
    new = "new"
    in_process = "in_process"
    finished = "finished"
