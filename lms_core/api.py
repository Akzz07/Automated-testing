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
    print("✅ Courses routes ditambahkan")
    main_router.add_router("courses/", courses_router)

    contents_router = Router()
    add_contents_routes(contents_router)
    print("✅ Contents routes ditambahkan")
    main_router.add_router("contents/", contents_router)

    comments_router = Router()
    add_comments_routes(comments_router)
    print("✅ Comments routes ditambahkan")
    main_router.add_router("comments/", comments_router)

    return main_router
