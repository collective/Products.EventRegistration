##get all email adresses to the registrants of the course
return ','.join([reg.email for reg in context.getFolderContents() if getattr(reg,'email','')!='']);
