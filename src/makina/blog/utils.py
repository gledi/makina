from faker import Faker

from .models import Post


def generate_fake_posts(num: int = 10) -> list[Post]:
    fake = Faker()
    posts = []
    for _ in range(num):
        is_published = fake.pybool()
        post = Post(
            title=fake.sentence()[:-1],
            body="\n\n".join(fake.paragraphs(10)),
            published_on=fake.date_time_this_month() if is_published else None,
            author=fake.name(),
            is_published=is_published,
            tags=fake.bs(),
        )
        posts.append(post)

    return posts
