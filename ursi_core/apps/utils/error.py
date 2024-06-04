class DataRetrievalError(Exception):
    pass

class ImageSaveError(Exception):
    pass

class VideoSaveError(Exception):
    pass

class ArchivoSaveError(Exception):
    pass

class CarpetasNotFoundError(Exception):
    pass
class CarpetaSlugNotFoundError(Exception):
    pass
class CarpetasSerializacionError(Exception):
    pass
class ImagenesNotFoundError(Exception):
    pass
class VideosNotFoundError(Exception):
    pass
class ArchivosNotFoundError(Exception):
    pass


class GetUserError(Exception):
    pass
class GetDataError(Exception):
    pass