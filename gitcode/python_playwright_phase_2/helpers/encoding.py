def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        print(
            *(str(a).encode("utf-8", errors="replace").decode() for a in args), **kwargs
        )
