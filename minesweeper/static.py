from pyramid.static import static_view

index_static_view = static_view('../public')
assets_static_view = static_view('../public/assets', use_subpath=True)
