from graphene import relay, Int
from django.forms.models import model_to_dict
from django.forms import ModelForm


class CustomNode(relay.Node):
    class Meta:
        name = 'Node'

    @staticmethod
    def to_global_id(type, id):
        return id

    @staticmethod
    def get_node_from_global_id(info, global_id, only_type=None):
        model = only_type._meta.model
        return model.objects.get(id=global_id)


def user_verification(modeldataUser, user):
    """[User Verification]
    you can use the convenient user_verification function which raises a PermissionDenied
    exception when the informed users are not equal each other.
    Args:
        modeldataUser ([object]): [It is related with the user in your specific model]
        user ([object]): [It is related with the authenticated user who made the request]
    Raises:
        Exception: [raises a PermissionDenied
    exception when the informed users are not equal each other.]
    Returns:
        [bollean]: [return True
    if the informed users are not equal each other.]
    """
    if modeldataUser != user:
        raise Exception("You do not have permission to perform this action!")
    return True


class CustomModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CustomModelForm, self).__init__(*args, **kwargs)

        # if form has being submitted and
        # model instance exists, then get data
        if self.is_bound and self.instance.pk:

            # get current model values
            modeldict = model_to_dict(self.instance)
            modeldict.update(self.data)

            # add instance values to data
            self.data = modeldict


        # if self.empty_permitted:
        # print(self.fields.items())
        for key, field in self.fields.items():
            if field.widget.is_required:
                field.widget.is_required = False
                field.required = False

class CustomConnection(relay.Connection):
    class Meta:
        abstract = True
        
    total_count = Int(description="Number of items in the queryset.",)
    edges_count = Int(description="Number of items in the edge list.",)

    def resolve_total_count(self, info):
        return self.iterable.count()
    
    def resolve_edges_count(self, info):
        return len(self.edges)