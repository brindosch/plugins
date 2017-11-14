# TEST REPOSITORY
Actually the api is just a DRAFT, so this is NOT USABLE. Comming when it's done.

## Hyperion Plugin Repository
This repository contains the source code for Hyperion Plugins. Plugins are small funtionality extensions for Hyperion written in Python. These plugins can be installed and configured from the Hyperion Web Configuration by any user worldwide.

## Plugin types
Currently there are 2 types of Plugins.
- Modul
- Service

A service plugin runs usually the whole time (if enabled), it starts and stops with the execution of Hyperion. Additional it has settings that can be configured from the user. \
A modul plugin provides utility methods which can be imported from a service plugin to be used. Examples are Python packages from the PyPi repository like simplejson or httplib2, which makes the developer life easier

## Contribute
You are free to add or improve any plugin that might be useful for other Hyperion users. This can be
- a integration of third party software or services
- a bridge between Hyperion and another device
- or whatever actually is spinning in your head

## Documentation
API documentation and more information can be found here: [Plugins Docu](https://docs.hyperion-project.org/en/developer/plugins)
