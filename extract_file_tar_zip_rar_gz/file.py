def extract_tar(data, output_dir):
    import tarfile
    from io import BytesIO
    with tarfile.open(fileobj=BytesIO(data), mode='r') as tar:
        tar.extractall(output_dir)

def extract_tar_gz(data, output_dir):
    import tarfile
    from io import BytesIO
    with tarfile.open(fileobj=BytesIO(data), mode='r:gz') as tar_gz:
        tar_gz.extractall(output_dir)

def extract_zip(data, output_dir):
    import zipfile
    from io import BytesIO
    with zipfile.ZipFile(BytesIO(data), 'r') as zip_file:
        zip_file.extractall(output_dir)

def extract_rar(data, output_dir):
    import rarfile
    from io import BytesIO
    with rarfile.RarFile(BytesIO(data), 'r') as rar:
        rar.extractall(output_dir)
