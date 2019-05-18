from django.apps import apps
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Generate create, update, details, list view from model(s)"

    def add_arguments(self, parser):
        parser.add_argument('app_label_and_models', nargs='+', type=str)

    def handle(self, *args, **options):
        app_label_and_models = self.parse_app_label_models(options['app_label_and_models'])
        print(app_label_and_models)

    @classmethod
    def parse_app_label_models(cls, param):
        app_models_dict = {}
        for p in param:
            app_label_model = p.split(':')
            app_label = app_label_model[0]

            if len(app_label_model) > 1:
                models = app_label_model[1].split(',')
            else:
                models = None

            app_config, models = cls.get_app_config_model_class(app_label, models)

            app_models_dict[app_label] = (models, app_config)
        return app_models_dict

    @classmethod
    def get_app_config_model_class(cls, app_label, models):
        try:
            app_config = apps.get_app_config(app_label)
        except:
            raise CommandError("No installed app with app label '%s'." % app_label)
        models = cls.get_models_app_label(app_config, models)
        return app_config, models

    @classmethod
    def get_models_app_label(cls, app_config, models):
        if models:
            try:
                return [app_config.get_model(model) for model in models]
            except:
                raise CommandError("One or more of the models you entered for '%s' are incorrect or not found." %
                                   app_config.label)
        else:
            raise CommandError("No models provides with app label '%s'." % app_config.label)
