def create_lms_router():
    from ninja import Router
    from lms_core.api_endpoints.auth import add_auth_routes
    from lms_core.api_endpoints.courses import add_courses_routes
    from lms_core.api_endpoints.contents import add_contents_routes
    from lms_core.api_endpoints.comments import add_comments_routes

    main_router = Router()

    auth_router = Router()
    add_auth_routes(auth_router)
    print("✅ Auth routes ditambahkan")
    main_router.add_router("auth/", auth_router)

    courses_router = Router()
    add_courses_routes(courses_router)
    add_contents_routes(courses_router)  # ⬅️ Tambah di sini
    add_comments_routes(courses_router)  # ⬅️ Dan ini juga
    print("✅ Courses, Contents, Comments routes ditambahkan")
    main_router.add_router("courses/", courses_router)

    return main_router
