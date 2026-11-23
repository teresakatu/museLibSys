from flask import redirect, request, url_for


def redirect_back(default_endpoint, anchor=None):
    target = request.form.get("next", "")
    if not target.startswith("/") or target.startswith("//") or "\\" in target:
        target = url_for(default_endpoint)
    if anchor:
        target = f"{target.split('#')[0]}#{anchor}"
    return redirect(target)
