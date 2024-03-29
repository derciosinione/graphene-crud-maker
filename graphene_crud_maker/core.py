import os
from django.apps import apps
from django.conf import settings


class CrudMaker(object):
    def __init__(self, app_name, exclude_fields):
        super(CrudMaker, self).__init__()
        self.app_name = app_name
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.APP_DIR = os.path.join(self.BASE_DIR, app_name)

        # Get All Django Models
        self.__all_models = [x.__name__ for x in apps.get_app_config(app_name).get_models()]
        django_settings_module = settings.SETTINGS_MODULE
        self.__settings_module = django_settings_module.split('.')[0]
        self.__exclude_fields = list(exclude_fields)
        self.__graphql_path = os.path.join(app_name, 'graphql')
        self.__base_path = os.path.join(self.BASE_DIR, 'graphene_crud_maker', 'base')
        self.list_import = list()
        self.list_class = list()

        self.__create_Api_folder(self.__graphql_path, self.__base_path)
        self.__create_queries(self.__base_path)
        self.__create_mutations(self.__base_path)
        self.__create_custom_schema(self.__base_path)
        self.__create_relay_query(self.__base_path)


    def __create_Api_folder(self, graphql_path, base_path):
        print(f'You called __create_Api_folder in {self.app_name} application')
        # Creating Directories : graphql, query, mutation
        if not os.path.exists(graphql_path):
            os.makedirs(os.path.join(graphql_path, 'query'))
            os.makedirs(os.path.join(graphql_path, 'mutation'))

        if not os.path.exists(os.path.join(graphql_path, '__init__.py')):
            with open(os.path.join(graphql_path, f'__init__.py'), 'w') as fw: pass

        if not os.path.exists(os.path.join(graphql_path, 'schema.py')):
            with open(os.path.join(base_path, f'BaseSchema.txt'), 'r') as fr:
                ### WRITING NEW schema FILE
                with open(os.path.join(graphql_path, 'schema.py'), 'w') as fw:
                    for line in fr.readlines():
                        if line.__contains__('App_'):
                            line = line.replace('App_', self.app_name)
                        fw.write(line)


    def __create_queries(self, base_path):
        print(f'You called Create queries in {self.app_name} application')
        query_path = os.path.join(self.__graphql_path, 'query')

        self.list_import.clear()
        self.list_class = ['class Query(ObjectType):\n',]

        for model in self.__all_models:
            self.list_import.append(f'from .{model} import {model}Type \n')

            self.list_class.append(f'\t{model.lower()} = CustomNode.Field({model}Type) \n')
            self.list_class.append(f'\tall_{model.lower()} = DjangoFilterConnectionField({model}Type) \n\n')

            # Verify if the current file already exist
            if not os.path.exists(os.path.join(query_path, f'{model}.py')):
                ### READING THE QUERY TXT
                with open(os.path.join(base_path, f'BaseQuery.txt'), 'r') as fr:
                    ### WRITING NEW QUERY FILE
                    with open(os.path.join(query_path, f'{model}.py'), 'w') as fw:
                        for line in fr.readlines():
                            if line.__contains__('Base_'):
                                line = line.replace('Base_', model)
                            if line.__contains__('App_'):
                                line = line.replace('App_', self.app_name)
                                print(line)
                            fw.write(line)


        # Writing __init__.py for queries
        with open(os.path.join(query_path, f'__init__.py'), 'w') as fw:
            fw.write('from graphene import ObjectType \n')
            fw.write(f'from {self.__settings_module}.schema.utils import CustomNode \n')
            fw.write('from graphene_django.filter import DjangoFilterConnectionField \n')
            fw.write('\n')

            for line in self.list_import:
                fw.write(line)

            fw.write('\n\n')

            for line in self.list_class:
                fw.write(line)

            fw.write('\n')
            self.list_class.clear()
            self.list_import.clear()

    def __create_custom_schema(self, base_path):
        module_path = self.__settings_module
        
        if not os.path.exists(os.path.join(module_path, 'schema')):
            os.makedirs(os.path.join(module_path, 'schema'))

        if not os.path.exists(os.path.join(module_path,'schema', 'schema.py')):
            with open(os.path.join(base_path, f'CoreSchema.txt'), 'r') as fr:
                ### WRITING NEW schema FILE
                with open(os.path.join(module_path,'schema', 'schema.py'), 'w') as fw:
                    for line in fr.readlines():
                        if line.__contains__('App_'):
                            line = line.replace('App_', self.app_name)
                        fw.write(line)

        
    def __create_relay_query(self, base_path):
        module_path = self.__settings_module
        
        if not os.path.exists(os.path.join(module_path, 'schema')):
            os.makedirs(os.path.join(module_path, 'schema'))

        if not os.path.exists(os.path.join(module_path,'schema', 'utils.py')):
            with open(os.path.join(base_path, f'BaseRelay.txt'), 'r') as fr:
                ### WRITING NEW utils FILE
                with open(os.path.join(module_path,'schema', 'utils.py'), 'w') as fw:
                    for line in fr.readlines():
                        fw.write(line)

        

    def __create_mutations(self, base_path):
        print('You called Create mutations')
        mutation_path = os.path.join(self.__graphql_path, 'mutation')
        self.list_import.clear()
        self.list_class = ['class Mutation(ObjectType):\n',]

        for model in self.__all_models:
            self.list_import.append(f'from .{model} import {model}Mutation, Remove{model} \n')

            self.list_class.append(f'\t{model.lower()} = {model}Mutation.Field() \n')
            self.list_class.append(f'\tremove_{model.lower()} = Remove{model}.Field() \n\n')

            # Verify if the current file already exist
            if not os.path.exists(os.path.join(mutation_path, f'{model}.py')):
                ### READING THE MUTATION TXT
                with open(os.path.join(base_path, f'BaseMutation.txt'), 'r') as fr:
                    ### WRITING NEW MUTATION FILE
                    with open(os.path.join(mutation_path, f'{model}.py'), 'w') as fw:
                        for line in fr.readlines():
                            if line.__contains__('Base_'):
                                line = line.replace('Base_', model)
                            if line.__contains__('App_'):
                                line = line.replace('App_', self.app_name)
                            if line.__contains__('pass_fields_'):
                                takedModel = apps.get_model(self.app_name, model)
                                field = sorted((field.name for field in takedModel._meta.concrete_fields))
                                excludeFields = []

                                for item in self.__exclude_fields:
                                    if field.__contains__(item):
                                        # field.remove(item)
                                        excludeFields.append(item)


                                # line = line.replace('pass_fields_', f'fields = {field}')
                                line = line.replace('pass_fields_', f'exclude = {excludeFields}')
                            fw.write(line)

        # Writing __init__.py for mutations
        with open(os.path.join(mutation_path, f'__init__.py'), 'w') as fw:
            fw.write('from graphene import ObjectType\n')
            fw.write('\n')

            for line in self.list_import:
                fw.write(line)

            fw.write('\n\n')

            for line in self.list_class:
                fw.write(line)

            self.list_class.clear()
            self.list_import.clear()

