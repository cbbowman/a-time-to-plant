from at2p_app.adapters.repositories import CropRepo


class CropInterface:
    def __init__(self, crop_repo: CropRepo) -> None:
        self._crop_repo = crop_repo

    def create_crop(self, init_dict):
        crop = self._crop_repo.create(init_dict)
        return crop

    def get_crop(self, crop_id):
        crop = self._crop_repo.get(crop_id)
        return crop

    def update_crop(self, crop):
        self._crop_repo.update(crop)
        return

    def delete_crop(self, crop):
        self._crop_repo.delete(crop)
        return
