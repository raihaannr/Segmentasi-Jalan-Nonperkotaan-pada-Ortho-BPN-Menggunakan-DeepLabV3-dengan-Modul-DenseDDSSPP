import os
import numpy as np
from PIL import Image

def crop_image(input_path, output_dir):
    """
    Memotong citra 800x800 menjadi empat bagian 512x512 piksel
    dari keempat sudut (kiri atas, kanan atas, kiri bawah, dan kanan bawah).
    
    Args:
        input_path (str): Path ke file citra input (TIFF)
        output_dir (str): Direktori untuk menyimpan hasil potongan citra
        
    Returns:
        bool: True jika berhasil, False jika gagal
    """
    try:
        # Baca citra input
        image = Image.open(input_path)
        
        # Pastikan ukuran citra adalah 800x800
        width, height = image.size
        if width != 800 or height != 800:
            print(f"Error: {os.path.basename(input_path)}: Ukuran citra harus 800x800 piksel. Ukuran saat ini: {width}x{height}")
            return False
        
        # Ukuran potongan
        crop_size = 512
        
        # Koordinat untuk pemotongan
        # Format: (left, upper, right, lower)
        crop_coords = [
            (0, 0, crop_size, crop_size),                # Kiri Atas
            (width - crop_size, 0, width, crop_size),    # Kanan Atas
            (0, height - crop_size, crop_size, height),  # Kiri Bawah
            (width - crop_size, height - crop_size, width, height)  # Kanan Bawah
        ]
        
        crop_names = ["kiri_atas", "kanan_atas", "kiri_bawah", "kanan_bawah"]
        
        # Dapatkan nama file tanpa ekstensi
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        # Potong dan simpan tiap bagian
        for i, (coords, name) in enumerate(zip(crop_coords, crop_names)):
            cropped = image.crop(coords)
            
            # Buat nama file output
            output_path = os.path.join(output_dir, f"{base_name}_{name}.tiff")
            
            # Simpan potongan citra
            cropped.save(output_path)
        
        print(f"Berhasil memotong citra: {os.path.basename(input_path)}")
        return True
    
    except Exception as e:
        print(f"Error memproses {os.path.basename(input_path)}: {str(e)}")
        return False

def process_folder(input_folder, output_folder):
    """
    Memproses semua file TIFF dalam folder input
    
    Args:
        input_folder (str): Path ke folder yang berisi citra-citra TIFF
        output_folder (str): Path ke folder untuk menyimpan hasil potongan
    """
    # Buat direktori output jika belum ada
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Daftar semua file di folder input
    files = os.listdir(input_folder)
    
    # Filter hanya file TIFF
    tiff_files = [f for f in files if f.lower().endswith(('.tiff', '.tif'))]
    
    if not tiff_files:
        print(f"Tidak ada file TIFF ditemukan di folder: {input_folder}")
        return
    
    print(f"Ditemukan {len(tiff_files)} file TIFF untuk diproses.")
    
    # Statistik
    successful = 0
    failed = 0
    
    # Proses setiap file TIFF
    for tiff_file in tiff_files:
        input_path = os.path.join(input_folder, tiff_file)
        if crop_image(input_path, output_folder):
            successful += 1
        else:
            failed += 1
    
    # Tampilkan ringkasan
    print(f"\nRingkasan Pemrosesan Pemotongan:")
    print(f"Total file yang diproses: {len(tiff_files)}")
    print(f"Berhasil: {successful}")
    print(f"Gagal: {failed}")

def rotate_images_in_folder(folder_path):
    """
    Merotasi gambar dalam folder berdasarkan nama file:
    - File dengan 'kanan_atas' dirotasi 90 derajat
    - File dengan 'kanan_bawah' dirotasi 180 derajat
    - File dengan 'kiri_bawah' dirotasi 270 derajat
    
    Args:
        folder_path (str): Path ke folder yang berisi gambar hasil potongan
    """
    print(f"\nMemulai proses rotasi gambar di {folder_path}")
    
    # Daftar semua file di folder
    files = os.listdir(folder_path)
    
    # Filter hanya file TIFF
    tiff_files = [f for f in files if f.lower().endswith(('.tiff', '.tif'))]
    
    # Statistik
    kanan_atas_count = 0
    kanan_bawah_count = 0
    kiri_bawah_count = 0
    
    for file in tiff_files:
        file_path = os.path.join(folder_path, file)
        
        try:
            # Buka gambar
            img = Image.open(file_path)
            
            # Tentukan derajat rotasi berdasarkan nama file
            if "kanan_atas" in file:
                img_rotated = img.rotate(-90, expand=False)  # 90 derajat searah jarum jam
                img_rotated.save(file_path)
                kanan_atas_count += 1
                print(f"Merotasi {file} sebesar 90 derajat")
                
            elif "kanan_bawah" in file:
                img_rotated = img.rotate(-180, expand=False)  # 180 derajat
                img_rotated.save(file_path)
                kanan_bawah_count += 1
                print(f"Merotasi {file} sebesar 180 derajat")
                
            elif "kiri_bawah" in file:
                img_rotated = img.rotate(-270, expand=False)  # 270 derajat searah jarum jam
                img_rotated.save(file_path)
                kiri_bawah_count += 1
                print(f"Merotasi {file} sebesar 270 derajat")
                
        except Exception as e:
            print(f"Error merotasi {file}: {str(e)}")
    
    # Tampilkan ringkasan
    print(f"\nRingkasan Rotasi:")
    print(f"File dengan 'kanan_atas' dirotasi 90°: {kanan_atas_count}")
    print(f"File dengan 'kanan_bawah' dirotasi 180°: {kanan_bawah_count}")
    print(f"File dengan 'kiri_bawah' dirotasi 270°: {kiri_bawah_count}")
    print(f"Total file dirotasi: {kanan_atas_count + kanan_bawah_count + kiri_bawah_count}")

# Contoh penggunaan
if __name__ == "__main__":
    # Ganti dengan path folder input dan output Anda
    input_folder = "input_images"
    output_folder = "output_crops"
    
    # Langkah 1: Potong semua citra di folder input
    process_folder(input_folder, output_folder)
    
    # Langkah 2: Rotasi gambar di folder output berdasarkan posisi
    rotate_images_in_folder(output_folder)