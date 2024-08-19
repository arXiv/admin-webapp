from pydantic_sqlalchemy_2 import sqlalchemy_to_pydantic

from arxiv.db.models import Document, Metadata, PaperPw, TapirUser, Demographic, \
    Endorsement, Submission, TapirEmailTemplate, EndorsementRequest, OwnershipRequest, \
    OwnershipRequestsAudit, PaperOwner, Category

# TapirEmailTemplateModel = sqlalchemy_to_pydantic(TapirEmailTemplate)
CategoryModel = sqlalchemy_to_pydantic(Category)
DocumentModel = sqlalchemy_to_pydantic(Document)
MetadataModel = sqlalchemy_to_pydantic(Metadata)
PaperPwModel = sqlalchemy_to_pydantic(PaperPw)
DemographicModel = sqlalchemy_to_pydantic(Demographic)
# EndorsementModel = sqlalchemy_to_pydantic(Endorsement)
# EndorsementRequestModel = sqlalchemy_to_pydantic(EndorsementRequest)
SubmissionModel = sqlalchemy_to_pydantic(Submission)

OwnershipRequestModel = sqlalchemy_to_pydantic(OwnershipRequest)
OwnershipRequestsAuditModel = sqlalchemy_to_pydantic(OwnershipRequestsAudit)
PaperOwnerModel = sqlalchemy_to_pydantic(PaperOwner)

# TapirUserModel = sqlalchemy_to_pydantic(TapirUser)
