import nbformat as nbf
from glob import glob

# Collect a list of all notebooks in the content folder
notebooks = glob("./*.ipynb", recursive=True)

# Text to look for in adding tags
text_search_dict = {
    # "# HIDDEN": "remove-cell",  # Remove the whole cell
    # "# NO CODE": "remove-input",  # Remove only the input
    "# @title": "hide-input"  # Hide the input w/ a button to show
}

# Search through each notebook and look for the text, add a tag if necessary
for ipath in notebooks:
    ntbk = nbf.read(ipath, nbf.NO_CONVERT)

    for cell in ntbk.cells:
        cell_tags = cell.get('metadata', {}).get('tags', [])
        for key, val in text_search_dict.items():
            if key in cell['source']:
                if val not in cell_tags:
                    cell_tags.append(val)
        if len(cell_tags) > 0:
            cell['metadata']['tags'] = cell_tags

        # Ensure that form cells are hidden by default
        if cell["cell_type"] == "code":
            first_line, *_ = cell["source"].splitlines()
            if "@title" in first_line or "@markdown" in first_line:
                cell["metadata"]["cellView"] = "form"

    nbf.write(ntbk, ipath)