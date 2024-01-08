# Yify
A Yify website clone, where users can view, search, and filter movies; registered users can also add movies. The modules that will be included in this project will be:

- User management.
- Movies management.
- Rating and review management.
- Request management.

This project was created with the purpose of learning about a Python framework called "Fast API".

## Getting started:
- Install [docker](https://www.docker.com/products/docker-desktop/).
- Create a file named as `.env` in the project root path, Add below varriables with their appropriate values.
    ```
    SECRET_KEY=
    PORT=

    DB_USER=
    DB_PASSWORD=
    DB_NAME=
    DB_HOST=
    DB_PORT=

    ACCESS_TOKEN_EXP_MINUTES=
    REFRESH_TOKEN_EXP_MINUTES=
    RESET_PASSWORD_EXP_MINUTES=

    FROM_EMAIL=
    SMTP_SERVER=
    SMTP_PORT=
    SMTP_USERNAME=
    SMTP_PASSWORD=
    DEFAULT_RECIPIENT_EMAIL=
    ```
- Run command: `docker-compose up`, To run the project.
- Fork the API collection from below link.

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/17396704-4bef6a1a-ae08-41b0-a358-738e44959abd?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D17396704-4bef6a1a-ae08-41b0-a358-738e44959abd%26entityType%3Dcollection%26workspaceId%3D392b781a-05ab-415b-9eb8-456aca6f3129)