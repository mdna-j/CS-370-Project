CREATE TABLE IF NOT EXISTS PetMedia(
    pet_media_ptr INTEGER PRIMARY KEY UNIQUE,
    pet_image_1 BLOB,
    pet_sound_1 BLOB,
    FOREIGN KEY (pet_media_ptr) REFERENCES PetState(Pet_ID) ON DELETE CASCADE
);