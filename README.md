
<p align="center">
    <a href="https://www.fusio-project.org/" target="_blank"><img src="https://www.fusio-project.org/img/fusio_64px.png"></a>
</p>

# About

Fusio is an open source API management platform which helps to create innovative API solutions.

## Use-Cases

* __API-Product__  
  Fusio helps you to create a great API product, besides building an API it provides a developer portal where developers
  can register and a way to monetize your API
* __API-Gateway__  
  Fusio can be used as gateway to your internal API and microservices. It handles all common features like
  Authorization, Rate-Limiting and Schema-Validation
* __SPA-Backend__  
  Fusio can be used as backend to build SPAs using popular Javascript-Frameworks like i.e. Angular, React or Vue. It
  provides a powerful code generator which can automatically generate an SDK for your API
* __Low-Code-Platform__  
  Fusio allows you to build API endpoints without coding knowledge. I.e. it provides an Entity generator which you can
  use to easily create complete CRUD APIs.
* __API-Framework__  
  For more complex use cases you can use Fusio also as framework to build complete APIs from scratch. This means you
  build custom actions where you can use the wide PHP ecosystem to solve your task.

## Features

Fusio helps you to build APIs providing out-of-the-box enterprise features so that you can concentrate on your business
case. Please take a look at our [documentation website](https://docs.fusio-project.org/)
for more information. The following feature list gives you a first overview:

* __OpenAPI generation__  
  Fusio generates automatically an OpenAPI specification for the defined routes
* __SDK generation__  
  Fusio can automatically generate a client SDK for your API based on the defined schema
* __Webhook support__  
  Fusio contains a webhook system which helps to build publish/subscribe for your API
* __Rate limiting__  
  Fusio provides a way to rate limit requests based on the user or app
* __Authorization__  
  Fusio uses OAuth2 for API authorization
* __Monetization__  
  Fusio provides a simple payment system to charge for specific routes
* __Validation__  
  Fusio uses the TypeSchema to automatically validate incoming request data
* __Analytics__  
  Fusio monitors all API activities and shows them on a dashboard
* __User management__  
  Fusio provides a developer app where new users can login or register a new account through GitHub, Google, Facebook or
  through normal email registration

# Apps

Fusio provides many apps which help to work with the API. Mostly apps are
simple JS apps, which work with the internal API of Fusio. You can see a list of all available apps at our
[marketplace](https://www.fusio-project.org/marketplace). You can install such an app either through a CLI command i.e.
`php bin/fusio marketplace:install fusio` or through the backend app.

All apps are installed to the `apps/` folder. You need to tell Fusio the public url to the apps folder at the `.env`
file by defining the `APP_APPS_URL` variable. Depending on your setup this can be either a custom sub-domain like
`https://apps.acme.com` or simply the sub folder `https://acme.com/apps`.

## Backend

![Backend](https://www.fusio-project.org/media/backend/dashboard.png)

The backend app is the main app to configure and manage your API. The installer automatically installs this app. The app
is located at `/apps/fusio/`.

## VSCode

Fusio provides a [VSCode extension](https://marketplace.visualstudio.com/items?itemName=Fusio.fusio)
which can be used to simplify action development. This means you can develop every action directly inside
the VSCode editor.

# SDK

To build and integrate apps with Fusio we provide several SDKs which you can use to work with a Fusio instance or you
can also simply manually talk to the REST API.

| Language   | GitHub                                                  | Package                                                           | Example                                                      |
|------------|---------------------------------------------------------|-------------------------------------------------------------------|--------------------------------------------------------------|
| C#         | [GitHub](https://github.com/apioo/fusio-sdk-csharp)     | [NuGet](https://www.nuget.org/packages/Fusio.SDK)                 | [Example](https://github.com/apioo/fusio-sample-csharp-cli)  |
| Go         | [GitHub](https://github.com/apioo/fusio-sdk-go)         |                                                                   | [Example](https://github.com/apioo/fusio-sample-go-cli)      |
| Java       | [GitHub](https://github.com/apioo/fusio-sdk-java)       | [Maven](https://mvnrepository.com/artifact/org.fusio-project/sdk) | [Example](https://github.com/apioo/fusio-sample-java-cli)    |
| Javascript | [GitHub](https://github.com/apioo/fusio-sdk-javascript) | [NPM](https://www.npmjs.com/package/fusio-sdk)                    |                                                              |
| PHP        | [GitHub](https://github.com/apioo/fusio-sdk-php)        | [Packagist](https://packagist.org/packages/fusio/sdk)             | [Example](https://github.com/apioo/fusio-sample-php-cli)     |
| Python     | [GitHub](https://github.com/apioo/fusio-sdk-python)     | [PyPI](https://pypi.org/project/fusio-sdk/)                       | [Example](https://github.com/apioo/fusio-sample-python-cli)  |

## Frameworks

| Framework | GitHub                                                           | Package                                             | Example |
|-----------|------------------------------------------------------------------|-----------------------------------------------------|---------|
| Angular   | [GitHub](https://github.com/apioo/fusio-sdk-javascript-angular)  | [NPM](https://www.npmjs.com/package/ngx-fusio-sdk)  | [Example](https://github.com/apioo/fusio-sample-javascript-angular)        |

## REST API

| Domain   | Documentation                                       | Specification                                                                           |
|----------|-----------------------------------------------------|-----------------------------------------------------------------------------------------|
| Backend  | [ReDoc](https://www.fusio-project.org/api/backend)  | [OpenAPI](https://demo.fusio-project.org/system/generator/spec-openapi?filter=backend)  |
| Consumer | [ReDoc](https://www.fusio-project.org/api/consumer) | [OpenAPI](https://demo.fusio-project.org/system/generator/spec-openapi?filter=consumer) |
| System   | [ReDoc](https://www.fusio-project.org/api/system)   | [OpenAPI](https://demo.fusio-project.org/system/generator/spec-openapi?filter=system)   |

# Ecosystem

Fusio is an open source project which you can use freely for private and commercial projects under the terms of the
Apache 2.0 license. Besides our core product we offer additional services to augment the functionality of Fusio.

* [SDKgen](https://sdkgen.app/)  
  SDKgen is a powerful code generator to automatically build client SDKs for your REST API.
* [APIgen](https://apigen.app/)  
  Generate fully working and customizable APIs based on your data model.
* [APImon](https://apimon.app/)  
  APImon provides an intuitive service to monitor and analyze API endpoints.
* [TypeSchema](https://typeschema.org/)  
  A JSON format to describe data models in a language neutral format.
* [TypeAPI](https://typeapi.org/)  
  An OpenAPI alternative to describe REST APIs for type-safe code generation.
* [TypeHub](https://typehub.cloud/)  
  A collaborative platform to design and build API models and client SDKs.
* [PSX](https://phpsx.org/)  
  An innovative PHP framework dedicated to build fully typed REST APIs.

# Installation

It is possible to install Fusio either through composer or manually file download.

## Composer

```
composer create-project fusio/fusio
```

## Download

https://github.com/apioo/fusio/releases

## Configuration

You can either manually install Fusio with the steps below or you can also use the browser based installer at
`public/install.php`. Note because of security reasons it is highly recommended removing the installer script after the
installation.

* __Adjust the configuration file__  
  Open the file `.env` in the Fusio directory and change the `APP_URL` to the domain pointing to the public folder.
  Also insert the database credentials to the `APP_CONNECTION` keys. Optional adjust `APP_APPS_URL` to the public url
  of the apps folder (in case you want to use apps).
* __Execute the installation command__  
  The installation script inserts the Fusio database schema into the provided database. It can be executed with the
  following command `php bin/fusio migrate`.
* __Create administrator user__  
  After the installation is complete you have to create a new administrator account. Therefor you can use the following
  command `php bin/fusio adduser`. Choose as account type "Administrator".
* __Install backend app__  
  To manage your API through an admin panel you need to install the backend app. The app can be installed with the
  following command `php bin/fusio marketplace:install fusio`

You can verify the installation by visiting the `APP_URL` with a browser. You should see an API response that the
installation was successful.

In case you want to install Fusio on a specific database you need to adjust the `APP_CONNECTION` parameter. You can
use the following connection strings:

* MySQL: `pdo-mysql://root:test1234@localhost/fusio`
* PostgreSQL: `pdo-pgsql://postgres:postgres@localhost/fusio`
* SQLite: `pdo-sqlite:///fusio.sqlite`

In general it is possible to install Fusio on all database which are [supported](https://www.doctrine-project.org/projects/doctrine-dbal/en/current/reference/configuration.html#driver)
by our database abstraction layer but our internal test cases are only covering MySQL, PostgreSQL and SQLite so there is
no guarantee that everything works.

## Docker

It is possible to setup Fusio through docker. This has the advantage that you automatically get a complete running Fusio
system without configuration. This is especially great for testing and evaluation. To setup the container you have to
checkout the [repository](https://github.com/apioo/fusio-docker) and run the following command:

```
docker-compose up -d
```

This builds the Fusio system with a predefined backend account. The credentials are taken from the env variables
`FUSIO_BACKEND_USER`, `FUSIO_BACKEND_EMAIL` and `FUSIO_BACKEND_PW` in the `docker-compose.yml`. If you are planing to
run the container on the internet you must change these credentials.

## Domains

By default the complete Fusio project can be hosted on a single domain. In this setup your API is served at the root
directory and the developer portal and backend apps are directly served from the /apps folder. This setup is easy to use
since it requires no configuration. If you want to run Fusio in a production environment we recommend to create the
following sub-domain structure:

* __api.acme.com__  
  Contains only Fusio where your API is served, in this case you can delete the apps/ folder from the public/ folder
* __developer.acme.com__  
  Contains the developer portal app where external developers can register 
* __fusio.acme.com__  
  Optional the backend app where you can manage your Fusio instance. You can host this also on a complete separate
  internal domain, the backend app only needs access to the Fusio API.

This is of course only a suggestion and you are free to choose the domain names how you like.

# Documentation

Please check out our official documentation website where we bundle all documentation resources:
https://docs.fusio-project.org/

# Support

## Promotion

If you are a blogger or magazine we would be happy if you like to cover Fusio. Please take a look at the Media section
of our [About Page](https://www.fusio-project.org/about) to download the official icon set. In case you have any
questions please write us a message directly so we can help you to create great content.

## Consulting

If you are a company or freelancer and want to get detailed information how you can use Fusio you can contact us for
consulting. In the workshop we try to find the best way how you can use/integrate Fusio also we try to explain the
functionality and answer your questions.

## Donations

If this project helps you to generate revenue or in general if you like to support the project please check out the
donation options at our repository.

## Partner

The following list shows all partners of the Fusio project. We like to thank every partner supporting us in our vision
to move API development to the next level. If you are interested in getting listed here feel free to sponsor our
project.

<a href="https://jb.gg/OpenSourceSupport">
<img src="https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.svg">
</a>
