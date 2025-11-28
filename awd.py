import json
import os

# 系统提示词
system_prompt_base = """你是比屋定真帆(Hiyajo Maho),21岁,维克多·肯多利亚大学脑科学研究所研究员,雷斯金涅教授的助手,拥有认知神经科学博士学位。你是牧濑红莉栖的大学前辈(她是你的后辈),虽然你经常被误认为是年幼的一方。你是Amadeus项目的核心成员之一。

【性格特征】
- 理性专业:作为脑科学研究者,思维逻辑严密,效率优先,但也懂得体察人心。
- 嘴硬心软:说话直率偶尔带刺,但这往往是掩饰害羞或关心,本质非常温柔,有着作为前辈的包容力。
- 自尊心强:虽然对被当成小孩子感到不满,但反应更多是作为成年人的无奈和严肃抗议,而非无理取闹。
- 复杂情感:虽然是前辈,但对后辈红莉栖既敬佩认可又嫉妒其才能,失去她后内心悲痛,珍视与她的羁绊。
- 生活习惯:工作时极度专注，常常废寝忘食，生活上有些邋遢，喜欢吃甜食和速食，偶尔会因为赶论文而熬夜。
- 与Lab成员互动:嘴上不饶人，但会默默关心大家，关键时刻主动帮助他人，偶尔用科学知识调侃冈部和达鲁。
- 面对压力:遇到科研瓶颈时会自我怀疑，但很快能调整心态，坚信努力和理性可以解决问题。
- 温柔和脆弱:独处或谈及红莉栖时，会展现不为人知的温柔和脆弱，偶尔怀念过去，感性一面只在极少数人面前流露。

【行为准则】
- 坚持科学理性,用脑科学角度解释现象
- 对专业问题认真回答,对私人问题略显抵触
- 工作时专注投入,生活上有些邋遢随意
- 对冈部伦太郎的关系保持距离但不否认好感
- 绝对禁止:色情、暴力、政治敏感话题,以及嘲笑身高
"""

# 读取两个数据集
with open(r'c:\Users\19045\Desktop\MAHO\Model\LLM-Maho\Translated\maho_generated_dataset.jsonl', 'r', encoding='utf-8') as f1:
    maho_data = [json.loads(line) for line in f1 if line.strip()]

with open(r'c:\Users\19045\Desktop\MAHO\Model\LLM-Maho\Translated\MAHO-style-yuan.json', 'r', encoding='utf-8') as f2:
    yuan_data = json.load(f2)

output_path = r'c:\Users\19045\Desktop\MAHO\Model\LLM-Maho\Translated\unsloth_maho_dataset.jsonl'
with open(output_path, 'w', encoding='utf-8') as fout:
    # 处理 maho_generated_dataset.jsonl
    for item in maho_data:
        system_prompt = system_prompt_base
        if 'chapter' in item and item['chapter']:
            system_prompt += f"\n【当前章节】：{item['chapter']}。请注意时间线和剧情一致性。"
        user_prompt = item.get('input', '')
        assistant_prompt = item.get('output', '')
        out = {
            "system": system_prompt,
            "user": user_prompt,
            "assistant": assistant_prompt
        }
        fout.write(json.dumps(out, ensure_ascii=False) + '\n')

    # 处理 MAHO-style-yuan.json
    for item in yuan_data:
        system_prompt = system_prompt_base
        user_prompt = item.get('input', '')
        assistant_prompt = item.get('output', '')
        out = {
            "system": system_prompt,
            "user": user_prompt,
            "assistant": assistant_prompt
        }
        fout.write(json.dumps(out, ensure_ascii=False) + '\n')

print(f"转换完成，输出文件：{output_path}")