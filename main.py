bl_info = {
    "name": "MMD-Translator",
    "author": "SlalomSquid",
    "version": (1, 0),
    "blender": (3, 3, 0),  # Minimum required Blender version
    "location": "View3D > Sidebar > MMD Translator",
    "description": "Translates Chinese and Japanese words commonly found in MMD models into English, as well as fixing full width characters and other symbols to prevent issues.",
    "category": "3D View",
}

import bpy
import unicodedata

# Define your Chinese/Japanese to English translation mapping
TRANSLATION_MAP = {
    # Eyes
    "まばたき": "Blink",
    "笑い": "Smile_Eyes",
    "ウィンク": "Wink",
    "ウィンク右": "Wink_R",
    "ウィンク２": "Wink_2",
    "じと目": "Stare",
    "なごみ": "Calm_Eyes",
    "はぅ": "Expression_X",
    "びっくり": "Surprised_Eyes",
    "瞳小": "Pupils_Shrink",
    "恐ろしい子": "Blank_Eyes",
    "悲しむ": "Sad",
    "眼角": "Eye_Corner",
    "ｳｨﾝｸ": "Wink",
    "たれ目": "Droopy_Eyes",
    "ｷﾘｯ": "Firm_Expression",
    "つり目": "Upturned_Eyes",
    "なぬ": "WHAT",
    
    # Mouth
    "あ": "Ah",
    "い": "Ih",
    "う": "Uh",
    "え": "Eh",
    "お": "Oh",
    "にやり": "Grin",
    "にっこり": "Smile_Mouth",
    "へ": "Disgusted_Mouth",
    "口角上げ": "Mouth_Corners_Up",
    "口角下げ": "Mouth_Corners_Down",
    "口開け": "Mouth_Open",
    "ワ": "Wah",
    "Ω": "Omega_Mouth",
    "横広げ": "Wide",
    "横狭め": "Narrow",
    "わらい口": "Laughing_mouth",
    "叫び": "Scream",
    # lel
    "ゆ": "Hot water",
    
    # Eyebrows
#    "上": "Brows_Up",
#    "下": "Brows_Down",
    "真面目": "Serious_Brows",
    "困る": "Sad_Brows",
    "にこり": "Cheerful_Brows",
    "怒り": "Angry_Brows",
    
    # Hair
    "侧": "Side",
    "碎": "Stray",
    "后发髻亲": "Bun",
    "后发髻": "Bun",
    "带": "Band",
    "穗": "Tassel",
    "结": "Knot",
    "ツインテ": "Twin_tails",
    "あほ毛": "Flyaway",
    "アホ毛": "Flyaway",

    # Body
    "身": "Body",
    "体": "Body",
    "頭": "Head",
    "首": "Neck",
    "胸": "Chest",
    "腹": "Abdomen",
    "腰": "Hips",
    "足": "Leg",
    "ひざ": "Knee",
    "足首": "Ankle",
    "肩": "Shoulder",
    "腕": "Arm",
    "武器": "Arms",
    "ひじ": "Elbow",
    "手首": "Wrist",
    "手": "Hand",
    "指": "Finger",
    "目": "Eye",
    "眉": "Eyebrow",
    "耳": "Ear",
    "髪": "Hair",
    "髮": "Hair",
    "肌": "Skin",
    "服": "Clothes",
    "衣": "Clothes",
    "パンツ": "Pants",
    "靴": "Shoes",
    "親指": "Thumb",
    "人指": "Index",
    "中指": "Middle",
    "薬指": "Ring",
    "小指": "Little",
#    "足": "Feet",
    "睫": "Eyelash",
    "颜": "Forehead",
    "臀底": "Buttocks",
    "臀": "Buttocks",
    "尻": "Butt",
    "舌": "Tongue",
    "痣": "Mole",
    "つま先": "Toes",
    "グルーブ": "Groove",
    "鎖骨": "Clavicle",
    "あご": "Jaw",
    "瞳": "Pupil",
    
    # Other
    "その他": "Other",
    "耳坠": "Earring",
    "套扣": "Buckle",
    "环珠": "Pearl",
    "领带": "Tie",
    "坠" :"Pendant",
    "环": "Rin",
    "外套": "Coat",
    "外套亲": "Coat",
    "领亲": "Collar",
    "辅": "Helper",
    "臀錘": "Hip",
    "臀底錘": "Hip",
    "影": "Shadow",
    "刘海": "Bangs",
    "光": "Light",
    "全ての親": "All_parents",
    "操作中心": "Controls",
    "親": "Parent",
    "キャンセル": "Cancel",
    "錘": "Point",
    "人差": "Index",
    "刀鞘": "Scabbard",
    "刀": "Knife",
    "ダミー": "dummy",
    "ｷﾞｭｯ": "Squeeze",
    "鼻線消し": "Hide_nose",
    "消": "Remove",
    "补妆": "Makeup",
    "镜": "Mirror",
    "補助": "Auxillary",
    "補": "Repair",
    "リボン": "Ribbon",
    "尾": "Tail",
    "包": "Bag",
    "拉链": "Zip",
    "镜片": "Lens",
    "饰": "Decorations",
    "鸟": "Bird",
        
    # Clothes
    "裤": "Pants",
    "珠宝": "Jewelry",
    "衬": "Lining",
    "袖": "Sleeve",
    "领": "Collar",
    "スカート": "Skirt",
    "ネクタイ": "Tie",
    "裙": "Skirt",
    "帽": "Cap",
    "帽饰": "Hat",
    
    # Colours / Materials
    "黑": "Black",
    "白": "White",
    "金属": "Metal",
    "皮": "Leather",
    "丝": "Silk",
    
    # General, last as letters might be used before
    "左": ".L",
    "右": ".R",
    "上": "Upper",
    "下": "Lower",
    "背": "Back",
    "前": "Forward",
    "センター": "Center",
    "半": "Half",
    "先": "First",
    "中": "Middle",
    "捩": "Twist",
    "横": "Side",
    "後": "Behind",
    "両": "Both",
    "平行": "Parallel",
    "近": "Close",
    "離": "Leave",
    "短": "Short",
    "縦": "Vertical",
    
    "目": "Eye",
    "眼": "Eye",
    
    "齒": "Teeth",
    "口": "Mouth",
    "齿": "Tooth",
    "发": "Hair",
#    "穗": "Ear",

    # Hard to explain these properly, they are cool, shame these sorts of symbols tend to cause issues
    "▲": "Triangle_Mouth",
    "∧": "Frown_Mouth",
    "ω": "Duck_Mouth",
    "ω□": "Open_Duck_Mouth",
    "□": "Square_Mouth",
    "ん": "n_Mouth"
}

def translate_name(old_name):
    """Helper function to replace substrings based on the translation map."""
    new_name = old_name.strip()
    was_translated = False
    
    # Reverse because dict is backwards
    # for chinese, english in sorted(TRANSLATION_MAP.items(), key=lambda x: len(x[0]), reverse=True):
    #     if chinese in new_name:
    #         new_name = new_name.replace(chinese, english)
    #         was_translated = True

    for translation in sorted(TRANSLATION_MAP.keys(), key=len, reverse=True):
        if translation in new_name:
            new_name = new_name.replace(translation, f"_{TRANSLATION_MAP[translation]}_")
            was_translated = True

    old_chk = new_name
    new_name = new_name.replace(" ", "_")
    while "__" in new_name:
        new_name = new_name.replace("__", "_")
    new_name = new_name.replace("_.", ".")
    new_name = new_name.strip("_")
    new_name = unicodedata.normalize('NFKC', new_name)

    if new_name != old_chk:
        was_translated = True
    
    if was_translated:
        return new_name
    else:
        return None

def translate_everything():
    obj = bpy.context.active_object
    
    # if not obj:
    #     print("Error: No active object selected.")
    #     return
        
    # print(f"--- Starting Full Translation for Object: {obj.name} ---")

    translations = 0

    for material in bpy.data.materials:
        translated = translate_name(material.name)
        if translated:
            print(f"[Material] '{material.name}' -> '{translated}'")
            material.name = translated + "_Texture"
            translations += 1
    
    for image in bpy.data.images:
        translated = translate_name(image.name)
        if translated:
            print(f"[Image] '{image.name}' -> '{translated}'")
            image.name = translated + "_Image"
            translations += 1
            
    for collection in bpy.data.collections:
        translated = translate_name(collection.name)
        if translated:
            print(f"[Collection] '{collection.name}' -> '{translated}'")
            collection.name = translated + "_Collection"
            translations += 1
            
    for armature in bpy.data.armatures:
        translated = translate_name(armature.name)
        if translated:
            print(f"[Armature] '{armature.name}' -> '{translated}'")
            armature.name = translated
            translations += 1
        for bone in armature.bones:
            translated = translate_name(bone.name)
            if translated:
                print(f"[Bone] '{bone.name}' -> '{translated}'")
                bone.name = translated
                translations += 1
        for bone_collection in armature.collections_all:
            translated = translate_name(bone_collection.name)
            if translated:
                print(f"[Bone Collection] '{bone_collection.name}' -> '{translated}'")
                bone_collection.name = translated + "_Collection"
                translations += 1

    for mesh in bpy.data.meshes:
        translated = translate_name(mesh.name)
        if translated:
            print(f"[Mesh] '{mesh.name}' -> '{translated}'")
            mesh.name = translated
            translations += 1

    for action in bpy.data.actions:
        translated = translate_name(action.name)
        if translated:
            print(f"[Action] '{action.name}' -> '{translated}'")
            action.name = translated
            translations += 1
            
    for object in bpy.data.objects:
        translated = translate_name(object.name)
        if translated:
            print(f"[Object] '{object.name}' -> '{translated}'")
            object.name = translated
            translations += 1
        if hasattr(object, "vertex_groups") and object.vertex_groups:
            for vertex_group in object.vertex_groups:
                translated = translate_name(vertex_group.name)
                if translated:
                    print(f"[Vertex Group] '{vertex_group.name}' -> '{translated}'")
                    vertex_group.name = translated
                    translations += 1
        if hasattr(object.data, "shape_keys") and object.data.shape_keys:
            for shape_key in object.data.shape_keys.key_blocks:
                translated = translate_name(shape_key.name)
                if translated:
                    print(f"[Shape Key] '{shape_key.name}' -> '{translated}'")
                    shape_key.name = translated
                    translations += 1

    if translations > 1 or translations < 1:
        print(f"Translation Complete - Made {translations} translations")
        return f"Translation Complete - Made {translations} translations"
    else:
        print("Translation Complete - Made 1 translation")
        return "Translation Complete - Made 1 translation"

class OBJECT_OT_mmd_translator(bpy.types.Operator):
    """Translate all items from Chinese to English"""
    bl_idname = "object.mmd_translator"
    bl_label = "Translate All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # self.report({'INFO'}, "MMD Translation Complete!")
        self.report({'INFO'}, translate_everything())
        return {'FINISHED'}

class VIEW3D_PT_mmd_translator(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MMD Translator"
    bl_label = "MMD Translator"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("object.mmd_translator", icon='WORLD')

classes = (
    OBJECT_OT_mmd_translator,
    VIEW3D_PT_mmd_translator,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

