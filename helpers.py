def get_filename(request_media):
    # Need to check if twitter URL filename= request_media.rstrip().split("/")[-1].split("?")[0]
    if "?" in request_media:
        retrieve_url = request_media.split("?")[0]
        # filename = file_prefix + request_media.rstrip().split("/")[-1].split("?")[0] + '.jpg'
    else:
        retrieve_url = request_media
        # filename = file_prefix + request_media.rstrip().split("/")[-1]

    filename = retrieve_url.rstrip().split("/")[-1]
    return filename