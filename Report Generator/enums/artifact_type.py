from enum import Enum


class ArtifactType(Enum):
    """
    Type of Imaging Artifacts
    """
    OBJECT = "object",
    SUB_OBJECT = "sub_object",
    RAW = "raw",

    @staticmethod
    def from_type(artifact_type: str):
        """
        Get the artifact from string
        :param artifact_type:  Type of the element
        :return: Corresponding ArtifactType
        """
        if artifact_type == "Object":
            return ArtifactType.OBJECT
        elif artifact_type == "SubObject":
            return ArtifactType.SUB_OBJECT
        elif artifact_type == "Raw":
            return ArtifactType.RAW
        else:
            raise KeyError("{0} doesn't exist in ArtifactType.".format(artifact_type))
