# Tramite-UTN-Bot

Notificador de nuevos movimientos de un trámite de UTN.

## Requisitos

* Disponer de un token de bot de Telegram
* Un chat ID de telegram al cual se enviarán las notificaciones.Hablandole previamente al bot, se puede encontrar en la respuesta de [getUpdates](https://core.telegram.org/bots/api#getupdates) como message.chat.id.
* El trámite debe poder trackearse desde la página [Gestión de Expedientes y Seguimiento de Trámites](http://xt.frba.utn.edu.ar/pub/login.do) con código y clave.

## Notas

Se sugiere utilizar Heroku para su deploy. La información sensible (tokens y claves) se puede almacenar fuera del código siguiendo [esta](https://devcenter.heroku.com/articles/config-vars#using-the-heroku-dashboard) guía.


