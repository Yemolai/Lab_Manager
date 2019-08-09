from LabManager import ma
from LabManager.dbModels import Person, User, FrequencyEvent, Inventory, Lendings, TechnicalIssues, Notices, FieldEvent

# Marshmellow schema definitions
class PersonSchema(ma.ModelSchema):
    class Meta:
        # fields = ('id', 'first_name', 'last_name', 'middle_name', 'phone', 'birthday', 'occupation', 'institution', 'imagefile', 'imagefile_path', 'type_id', 'genre_id')
        model = Person

class UserSchema(ma.ModelSchema):
    class Meta:
        # fields = ('id', 'username', 'email', 'person_id', 'notices')
        model = User

class FrequencySchema(ma.ModelSchema):
    class Meta:
        # fields = ('id', 'date', 'entry_time', 'exit_time', 'person_id')
        model = FrequencyEvent

class InventorySchema(ma.ModelSchema):
    class Meta:
        # fields = ('id', 'name', 'description', 'imagefile', 'imagefile_path', 'lendings', 'issues', 'field_events')
        model = Inventory

class LendingSchema(ma.ModelSchema):
    class Meta:
        # fields = ('id', 'lend_date', 'return_expected', 'return_done', 'observations', 'inventory_id')
        model = Lendings

class IssueSchema(ma.ModelSchema):
    class Meta:
        # fields = ('id', 'description', 'report_date', 'solution_date', 'equipment_id')
        model = TechnicalIssues

class NoticeSchema(ma.ModelSchema):
    class Meta:
        # fields = ('id', 'title', 'date', 'content', 'archived', 'user_id')
        model = Notices

class FieldSchema(ma.ModelSchema):
    class Meta:
        # fields = ('id', 'location', 'date_start', 'date_end_expected', 'date_end_done', 'observations')
        model = FieldEvent


# Marshmallow schema inits
person_schema = PersonSchema(strict=True)
persons_schema = PersonSchema(many=True, strict=True)
user_schema = UserSchema(strict=True)
frequency_schema = FrequencySchema(strict=True)
equipment_schema = InventorySchema(strict=True)
equipments_schema = InventorySchema(many=True, strict=True)
lending_schema = LendingSchema(strict=True)
lendings_schema = LendingSchema(many=True, strict=True)
issue_schema = IssueSchema(strict=True)
issues_schema = IssueSchema(many=True, strict=True)
notice_schema = NoticeSchema(strict=True)
notices_schema = NoticeSchema(many=True, strict=True)
field_schema = FieldSchema(strict=True)
fields_schema = FieldSchema(many=True, strict=True)
