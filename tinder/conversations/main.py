import asyncio
from aiohttp import web
# ai
from deeppavlov import configs, train_model
from deeppavlov.core.common.file import read_json

model_config = read_json(configs.faq.tfidf_logreg_en_faq)
model_config["dataset_reader"]["data_path"] = "faq.csv"
model_config["dataset_reader"]["data_url"] = None
faq = train_model(model_config)


async def getrec(request):
    request_json = await request.json()
    msg = request_json["text"]
    a = faq([msg])
    return web.json_response({"text": a})


async def init_app():
    app = web.Application()
    app.router.add_route("POST", "/api/getrec", getrec)
    return app

loop = asyncio.get_event_loop()
app = loop.run_until_complete(init_app())
web.run_app(app, port=9009)
