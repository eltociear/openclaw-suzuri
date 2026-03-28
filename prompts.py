"""OpenClaw デザインプロンプト管理

OpenClaw = ロブスターを被った猫（Claw = ロブスターの爪）
全デザインがこのキャラクターを軸に展開される
"""
import random

# OpenClawキャラクター定義
OPENCLAW_BASE = "a cute cat wearing a lobster costume on its head, lobster claw hat, cat with lobster headgear"

# スタイルテンプレート（{character}にOpenClaw猫が入る）
TEMPLATES = [
    "{character}, minimalist vector art, clean lines, white background, t-shirt print design, high quality illustration",
    "{character}, cute kawaii style, pastel colors, simple flat design, sticker style, transparent background, adorable",
    "{character}, retro vintage poster style, bold typography, screen print aesthetic, limited color palette",
    "{character}, watercolor painting style, artistic splash, soft colors, creative composition",
    "{character}, japanese ukiyo-e inspired illustration, modern twist, traditional meets contemporary",
    "{character}, neon glow cyberpunk aesthetic, dark background, vivid colors, futuristic",
    "{character}, hand drawn ink illustration, detailed linework, monochrome with red accent color",
    "{character}, pop art style, bold colors, halftone dots, comic book aesthetic, eye-catching",
    "{character}, pixel art retro gaming style, 8-bit aesthetic, nostalgic, colorful sprites",
    "{character}, chibi anime style, big eyes, small body, super cute, expressive",
]

# シチュエーション（OpenClaw猫が何をしているか）
SITUATIONS = {
    "daily_life": [
        "sitting elegantly",
        "sleeping curled up",
        "stretching and yawning",
        "playing with yarn",
        "drinking coffee at a cafe",
        "reading a book",
        "taking a selfie",
        "riding a bicycle",
        "cooking in a kitchen",
        "working at a computer",
    ],
    "adventure": [
        "surfing on a big wave",
        "exploring outer space in a rocket",
        "climbing a mountain peak",
        "diving underwater with fish",
        "flying with balloons",
        "skateboarding in the city",
        "camping under the stars",
        "sailing on a tiny boat",
        "riding a skateboard",
        "parachuting from the sky",
    ],
    "seasonal": [
        "under cherry blossoms in spring",
        "at the beach in summer with sunglasses",
        "surrounded by autumn leaves",
        "playing in the snow in winter",
        "watching fireworks at a festival",
        "trick or treating on Halloween",
        "opening Christmas presents",
        "celebrating New Year with mochi",
        "enjoying hanami picnic",
        "holding an umbrella in the rain",
    ],
    "japanese_culture": [
        "eating ramen at a street stall",
        "sitting in an onsen hot spring",
        "wearing a kimono",
        "practicing zen meditation",
        "at a sushi conveyor belt",
        "at a matsuri festival with lanterns",
        "in front of Mount Fuji",
        "at a torii gate shrine",
        "making takoyaki",
        "riding the shinkansen",
    ],
    "funny": [
        "pretending to be a DJ at turntables",
        "lifting tiny weights at a gym",
        "as a sushi chef with a knife",
        "conducting an orchestra",
        "painting a self-portrait",
        "winning a trophy proudly",
        "dressed as a superhero flying",
        "meditating and floating",
        "boxing with lobster claws",
        "doing karate with lobster claws as weapons",
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
        raw_template_str は再現性のために返却（通常は使用しない）
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
    "realistic human, photograph"
)
