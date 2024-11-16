def validate_provider_name(name):
    if not name or not isinstance(name, str):
        raise ValueError("Provider name must be a non-empty string.")
