import schemas


from sqlalchemy.orm import Session


async def process_document_in_ai(
    db: Session, document: schemas.Document
) -> schemas.OpenAIResponse:
    response = schemas.OpenAIResponse(
        Determination="Denied",
        Reasoning="Reasoning:\n\n1. The CPT code 3288F is a performance measure code used for reporting purposes only. It is not a reimbursable service, hence it is not covered by insurance.\n\n2. The ICD-10 codes provided, B35.1 (Tinea unguium) and M72.2 (Plantar fascial fibromatosis), do not align with the CPT code 3288F. The CPT code 3288F is used to report the percentage of patients aged 18 years and older with a diagnosis of COPD (Chronic Obstructive Pulmonary Disease) who have an FEV1/FVC less than 70% and have symptoms of dyspnea.\n\n3. The ICD-10 codes B35.1 and M72.2 are related to dermatological and musculoskeletal conditions respectively, not respiratory conditions. Therefore, these diagnoses do not support the use of the CPT code 3288F.\n\n4. The claim lacks the necessary documentation to support the medical necessity of the service provided. The insurance policy requires that the services provided must be medically necessary and appropriate for the diagnosis.\n\n5. The claim does not meet the insurance policy's coverage criteria for the CPT code 3288F. The policy requires that the CPT code and the ICD-10 codes must be compatible and the service provided must be covered under the policy.\n\nDue to these reasons, the claim for CPT code 3288F with ICD-10 codes B35.1 and M72.2 is denied.",
        Query="The Claim for CPT code 3288F with ICD-10 codes: B35.1 M72.2",
        Context="",
        Raw_Output="Determination: Denied\n\nReasoning:\n\n1. The CPT code 3288F is a performance measure code used for reporting purposes only. It is not a reimbursable service, hence it is not covered by insurance.\n\n2. The ICD-10 codes provided, B35.1 (Tinea unguium) and M72.2 (Plantar fascial fibromatosis), do not align with the CPT code 3288F. The CPT code 3288F is used to report the percentage of patients aged 18 years and older with a diagnosis of COPD (Chronic Obstructive Pulmonary Disease) who have an FEV1/FVC less than 70% and have symptoms of dyspnea.\n\n3. The ICD-10 codes B35.1 and M72.2 are related to dermatological and musculoskeletal conditions respectively, not respiratory conditions. Therefore, these diagnoses do not support the use of the CPT code 3288F.\n\n4. The claim lacks the necessary documentation to support the medical necessity of the service provided. The insurance policy requires that the services provided must be medically necessary and appropriate for the diagnosis.\n\n5. The claim does not meet the insurance policy's coverage criteria for the CPT code 3288F. The policy requires that the CPT code and the ICD-10 codes must be compatible and the service provided must be covered under the policy.\n\nDue to these reasons, the claim for CPT code 3288F with ICD-10 codes B35.1 and M72.2 is denied.",
    )
    return response
