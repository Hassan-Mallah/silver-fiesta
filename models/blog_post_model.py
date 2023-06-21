# create project BaseModels models here

from pydantic import BaseModel


class BlogPost(BaseModel):
    """ blog post data """

    title: str
    content: str
