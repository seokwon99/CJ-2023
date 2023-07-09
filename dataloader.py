import random
from tqdm import tqdm
import pandas as pd

class DataLoader:
    
    def __init__(self, data_path, num=200000):
        from template import EXTRA_WORDS, SEP_TOKENS, UNDERGROUND
        data = self._raw_data_loader(data_path)
        data = self._preprocess(data)
        template = self._load_template()
        sources = []
        targets = []
        
        data = random.sample(data, num)
        for sample in tqdm(data):
            inp_dict = dict()
            inp_dict.update(sample)
            inp_dict.update({"추가": random.choice(EXTRA_WORDS)})
            inp_dict.update({"건물본번1": sample["지하여부1"]+sample['건물본번']})
            inp_dict.update({"건물본번1": sample["지하여부2"]+sample['건물본번']})                
            noi_temp = random.choice(template['noised']).split(" ")
            tar_temp = template['target'].split(" ")
            
            if sample['읍면동명'].endswith('읍') or sample['읍면동명'].endswith('면'):
                tar_temp.insert(2, "{읍면동명}")
            if sample['건물부번'] == "0":
                tar_temp = [t if t != '{건물본번1}-{건물부번}' else '{건물본번1}' for t in tar_temp]
                noi_temp = [t if t != '{건물본번2}-{건물부번}' else '{건물본번2}' for t in noi_temp]
                
            noi_temp = random.choice(SEP_TOKENS).join(tar_temp)
            tar_temp = " ".join(tar_temp)

            sources.append(noi_temp.format_map(inp_dict))
            targets.append(tar_temp.format_map(inp_dict))
        self.sources, self.targets = self._noising(sources, targets)
    
    def __getitem__(self):
        data = {
            "input": self.sources,
            "output": self.targets
        }
        return pd.DataFrame(data)
    
    def _raw_data_loader(self, file_path):
        import json
        with open(file_path) as f:
            data = json.load(f)
        return data

    def _preprocess(self, data):
        new_data = []
        for d in data:
            if len(data[d].keys()) == 3:
                new_in = dict()
                new_in.update(data[d]['k_doro'])
                new_in.update(data[d]['k_zibun'])
                new_in.update(data[d]['e_doro'])
                new_in["지하여부1"] = "B" if new_in["지하여부"] == "1" else ""
                new_in["지하여부2"] = random.choice(["B", "GF", "G/F"]) if new_in["지하여부"] == "1" else ""
                new_data.append(new_in)
        return new_data

    def _load_template(self):
        from template import TEMPLATE, ENTITY_MATCH
        def get_combinations(lst):
            from itertools import combinations
            combinations_list = []
            for r in range(len(lst) + 1):
                combinations_list.extend(combinations(lst, r))
            return combinations_list
        
        new_template = []
        for t in TEMPLATE['noised']:
            for d in get_combinations(ENTITY_MATCH.keys()):
                tt = t
                for k in d:
                    tt = tt.replace(k, ENTITY_MATCH[k])

                tt_l = tt.split(' ')
                random_index = random.randint(0, len(tt_l))
                tt_l.insert(random_index, "{추가}")    
                
                new_template.append(tt)
                new_template.append(' '.join(tt_l))
                
        TEMPLATE['noised'] = new_template
        return TEMPLATE

    def _noising(self, sources, targets, prob=.3):
        from konoise import NoiseGenerator
        """
        konoise 라이브러리 활용 (https://pypi.org/project/konoise/)
        
        [original]  행복한 가정은 모두가 닮았지만, 불행한 가정은 모두 저마다의 이유로 불행하다.

        [disattach-letters, prob=1.] 행복한 ㄱㅏ정은 모두ㄱㅏ 닮았ㅈㅣ만, 불행한 ㄱㅏ정은 모두 ㅈㅓㅁㅏㄷㅏ의 ㅇㅣ유로 불행ㅎㅏㄷㅏ.

        [change-vowels, prob=1.] 행복한 갸정은 묘듀갸 닮았지만, 불행한 갸정은 묘듀 져먀댜의 이우료 불행햐댜.

        [palatalization, prob=1.] 행보칸 가정은 모두가 닮았지만, 불행한 가정은 모두 저마다의 이유로 불행하다.

        [linking, prob=1.] 행복한 가정은 모두가 달맜지만, 불행한 가정은 모두 저마다의 이유로 불행하다.

        [liquidization, prob=1.] 행복한 가정은 모두가 닮았지만, 불행한 가정은 모두 저마다의 이유로 불행하다.(No Change)

        [nasalization, prob=1.] 행복한 가정은 모두가 닮았지만, 불행한 가정은 모두 저마다의 이유로 불행하다. (No Change)

        [assimilation, prob=1.] 행복한 가정은 모두가 닮았지만, 불행한 가정은 모두 저마다의 이유로 불행하다. (No Change)

        [yamin-jungum, prob=1.] 행복한 가정은 모두가 닮았지만, 불행한 가정은 모두 저마다의 이윾로 불행하다.
        """
        
        new_sources = []
        
        generator = NoiseGenerator(num_cores=8)
        
        for source in sources:  
            noised_source = source
            for method in ["palatalization", "liquidization", "nasalization", "assimilation", "linking", "disattach-letters", "change-vowels", "yamin-jungum"]:
                noised_source = generator.generate(noised_source, methods=method, prob=prob)
            noised_source = noised_source
            new_sources.append(noised_source)
        
        return sources, targets
        
def main():
    df = DataLoader('combined.json').__getitem__()
    df.to_csv('train.csv', sep=',', na_rep='NaN')

if __name__ == "__main__":
    main()
