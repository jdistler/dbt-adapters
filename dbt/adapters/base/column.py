def from_description(cls, name: str, raw_data_type: str) -> "Column":
    match = re.match(r"([^(]+)(\([^)]+\))?", raw_data_type)
    if match is None:
        raise DbtRuntimeError(f'Could not interpret data type "{raw_data_type}"')
    
    data_type, size_info = match.groups()
    char_size, numeric_precision, numeric_scale = None, None, None

    if size_info is not None:
        # strip out the parentheses
        size_info = size_info[1:-1]

        # If it contains a nested type structure, ignore further size processing
        if not re.search(r"[A-Z]+\(", size_info):
            parts = size_info.split(",")
            
            if len(parts) == 1:
                try:
                    char_size = int(parts[0])
                except ValueError:
                    raise DbtRuntimeError(
                        f'Could not interpret data_type "{raw_data_type}": '
                        f'could not convert "{parts[0]}" to an integer'
                    )
            elif len(parts) == 2:
                try:
                    numeric_precision = int(parts[0])
                    numeric_scale = int(parts[1])
                except ValueError as e:
                    part_idx = 0 if 'first' in str(e) else 1
                    raise DbtRuntimeError(
                        f'Could not interpret data_type "{raw_data_type}": '
                        f'could not convert "{parts[part_idx]}" to an integer'
                    )

    return cls(name, data_type, char_size, numeric_precision, numeric_scale)
