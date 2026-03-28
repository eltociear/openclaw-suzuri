"""OpenClaw デザインプロンプト管理

OpenClaw = ロブスターの着ぐるみを着た白い子猫
全デザインがこのキャラクターを軸に展開される
"""
import random

# OpenClawキャラクター定義（参考画像のテイストに完全準拠）
OPENCLAW_BASE = (
    "an adorable fluffy white kitten wearing a full red lobster costume, "
    "lobster shell covering its body, big lobster claws as hands, "
    "lobster eyes on stalks on top of the head, lobster tail behind, "
    "the kitten has huge round brown eyes, tiny pink nose, soft white fur, "
    "chibi proportions, round chubby body, sitting cutely, "
    "digital painting, smooth rendering, 3D-like shading, "
    "clean white background, t-shirt print design, centered composition, "
    "high detail, professional illustration"
)

# スタイルバリエーション（全てベースのテイストを維持しつつ微変化）
TEMPLATES = [
    "{character}, front facing, looking at viewer with innocent eyes",
    "{character}, slight head tilt, curious expression, one paw raised",
    "{character}, happy smile, eyes sparkling, playful pose",
    "{character}, sleepy expression, half-closed eyes, cozy feeling",
    "{character}, surprised expression, wide eyes, mouth slightly open",
    "{character}, winking, cheerful, one eye closed playfully",
    "{character}, determined expression, clenching lobster claws, confident pose",
    "{character}, shy expression, blushing cheeks, looking down cutely",
    "{character}, excited expression, both claws raised up, celebrating",
    "{character}, peaceful expression, eyes gently closed, serene smile",
]

# シチュエーション（OpenClaw猫が何をしているか）
SITUATIONS = {
    "daily_life": [
        "sitting elegantly",
        "sleeping curled up",
        "stretching and yawning",
        "playing with yarn",
        "drinking coffee from a tiny cup",
        "reading a small book",
        "taking a selfie with phone",
        "riding a tiny bicycle",
        "wearing a chef hat and cooking",
        "sitting at a tiny computer",
    ],
    "adventure": [
        "surfing on a big wave",
        "floating in outer space with stars",
        "standing on a mountain peak with flag",
        "diving underwater with tropical fish",
        "flying with colorful balloons",
        "riding a skateboard",
        "camping with a tiny tent",
        "sailing on a paper boat",
        "riding on a rocket",
        "parachuting with a tiny parachute",
    ],
    "seasonal": [
        "under cherry blossom petals falling",
        "at the beach wearing sunglasses",
        "surrounded by falling autumn leaves",
        "playing in fluffy snow",
        "watching colorful fireworks",
        "wearing a tiny Halloween costume",
        "next to a Christmas tree with presents",
        "eating mochi for New Year",
        "having a hanami picnic with dango",
        "holding a tiny umbrella in rain",
    ],
    "japanese_culture": [
        "eating ramen from a big bowl",
        "relaxing in an onsen hot spring",
        "wearing a cute mini kimono",
        "meditating peacefully in zen style",
        "sitting at a sushi conveyor belt",
        "holding a festival lantern",
        "posing in front of Mount Fuji",
        "standing at a red torii gate",
        "making takoyaki with a pick",
        "riding a tiny shinkansen",
    ],
    "funny": [
        "pretending to be a DJ with turntables",
        "lifting tiny dumbbells at a gym",
        "wearing a sushi chef headband with knife",
        "conducting an orchestra with a baton",
        "painting a self-portrait on canvas",
        "holding a golden trophy proudly",
        "wearing a tiny superhero cape flying",
        "floating in meditation pose with sparkles",
        "boxing pose with lobster claws ready",
        "doing karate kick with lobster claws",
    ],
}


def get_all_situations() -> list[str]:
    """全シチュエーションをフラットなリストで取得"""
    all_situations = []
    for situations in SITUATIONS.values():
        all_situations.extend(situations)
    return all_situations


def build_prompt(situation: str, style_index: int = None) -> str:
    """OpenClaw猫 + シチュエーション + スタイルでプロンプト構築"""
    character = f"{OPENCLAW_BASE}, {situation}"
    if style_index is not None:
        template = TEMPLATES[style_index % len(TEMPLATES)]
    else:
        template = random.choice(TEMPLATES)
    return template.format(character=character)


def random_prompt() -> tuple[str, str, str]:
    """ランダムなプロンプトを生成

    Returns:
        (rendered_prompt, situation, raw_template_str) のタプル
    """
    situation = random.choice(get_all_situations())
    template = random.choice(TEMPLATES)
    character = f"{OPENCLAW_BASE}, {situation}"
    prompt = template.format(character=character)
    return prompt, situation, template


# ネガティブプロンプト
NEGATIVE_PROMPT = (
    "blurry, low quality, text, watermark, signature, "
    "deformed, ugly, duplicate, morbid, mutilated, "
    "poorly drawn, bad anatomy, wrong proportions, "
    "extra limbs, cloned face, disfigured, gross proportions, "
    "malformed limbs, missing arms, missing legs, "
    "extra arms, extra legs, fused fingers, too many fingers, "
    "long neck, username, error, worst quality, "
    "realistic human, photograph, dark background, "
    "complex background, busy background, multiple characters"
)
