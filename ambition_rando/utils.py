from ambition_sites import ambition_sites


def get_site_name(long_name, row=None):
    """Returns the site name given the "long" site name.
    """
    try:
        site_name = [site for site in ambition_sites if site[2] == long_name][0][1]
    except IndexError as e:
        raise IndexError(f"{long_name} not found. Got {e}. See {row}")
    return site_name
