import random
from tqdm import tqdm
import pandas as pd
import argparse

class DataLoader:
    
    def __init__(self, data_path, min_repeat=1, max_repeat=1, num=50000):
        from template import EXTRA_WORDS, SEP_TOKENS
        data = self._raw_data_loader(data_path)
        data = self._preprocess(data)
        address_tree = self._get_tree(data)
        template = self._load_template()
        sources = []
        targets = []
        for _ in tqdm(range(num)):
            now = address_tree
            while True:
                if isinstance(now, list):
                    sample_key = random.choice(now)
                    sample = data[sample_key]
                    break
                
                next_key = random.choice(list(now.keys()))
                now = now[next_key]
            
            inp_dict = dict()
            inp_dict.update(sample)
            inp_dict.update({"추가": random.choice(EXTRA_WORDS)})
            inp_dict.update({"건물본번1": sample["지하여부1"]+sample['건물본번']})
            inp_dict.update({"건물본번2": sample["지하여부2"]+sample['건물본번']})                
            noi_temp = random.choice(template['noised']).split(" ")
            tar_temp = template['target'].split(" ")
            
            if sample['읍면동명'].endswith('읍') or sample['읍면동명'].endswith('면'):
                tar_temp.insert(2, "{읍면동명}")
                tar_temp = tar_temp[:-1]
            
            if sample['건물부번'] == "0":
                tar_temp = [t if t != '{건물본번1}-{건물부번}' else '{건물본번1}' for t in tar_temp]
                noi_temp = [t if t != '{건물본번2}-{건물부번}' else '{건물본번2}' for t in noi_temp]
            
            repeated_noi_temp = []
            for e in noi_temp:
                rand_repeat = random.choice(range(min_repeat, max_repeat+1))
                repeated_noi_temp.extend([e for _ in range(rand_repeat)])
            random.shuffle(repeated_noi_temp)
                
            
            if '{시도명}' not in repeated_noi_temp and '{영문시도명}' not in repeated_noi_temp:
                tar_temp.remove('{시도명}')
            if '{시군구명}' not in repeated_noi_temp and '{영문시군구명}' not in repeated_noi_temp:
                tar_temp.remove('{시군구명}')
            if '{도로명}' not in repeated_noi_temp and '{영문도로명}' not in repeated_noi_temp:
                tar_temp.remove('{도로명}')
            if '{건물본번2}-{건물부번}' not in repeated_noi_temp and '{건물본번1}-{건물부번}' in tar_temp:
                tar_temp.remove('{건물본번1}-{건물부번}')
            if '{건물본번2}' not in repeated_noi_temp and '{건물본번1}' in tar_temp:
                tar_temp.remove('{건물본번1}')
            if '({행정동명})' not in repeated_noi_temp and '({행정동명})' in tar_temp:
                tar_temp.remove('({행정동명})')
            if '{읍면동명}' not in repeated_noi_temp and '{읍면동명}' in tar_temp:
                tar_temp.remove('{읍면동명}')
            
            repeated_noi_temp = random.choice(SEP_TOKENS).join(repeated_noi_temp).replace('({행정동명})', '{행정동명}')
            tar_temp = " ".join(tar_temp)

            sources.append(repeated_noi_temp.format_map(inp_dict))
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
        new_data = {}
        for d in tqdm(data):
            if len(data[d].keys()) == 3:
                new_in = dict()
                new_in.update(data[d]['k_doro'])
                new_in.update(data[d]['k_zibun'])
                new_in.update(data[d]['e_doro'])
                new_in["지하여부1"] = "B" if new_in["지하여부"] == "1" else ""
                new_in["지하여부2"] = random.choice(["B", "GF", "G/F"]) if new_in["지하여부"] == "1" else ""
                new_data[d] = new_in
        return new_data

    def _get_tree(self, data):
        address_tree = {}
        add_keys = ["시도명", "시군구명", "읍면동명", "리명", "도로명", "행정동명"]
        for key in tqdm(data):
            sample = data[key]
            now = address_tree
            for add_key in add_keys:
                element = sample[add_key]
                if element not in now:
                    if add_key == "행정동명":
                        now[element] = []
                    else:
                        now[element] = {}
                now = now[element]
            now.append(key)
        return address_tree
    
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
        """
        from konoise import NoiseGenerator
        
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
        
        
        new_sources = []
        
        generator = NoiseGenerator(num_cores=8)
        
        for source in sources:  
            noised_source = source
            for method in ["palatalization", "liquidization", "nasalization", "assimilation", "linking", "disattach-letters", "change-vowels", "yamin-jungum"]:
                noised_source = generator.generate(noised_source, methods=method, prob=prob)
            noised_source = noised_source
            new_sources.append(noised_source)
        """
        return sources, targets
        
def parse():
    parser = argparse.ArgumentParser(description="A simple example of argparse usage.")
    
    parser.add_argument("--input", default="processed/combined.json", help="Path to the input file.")
    parser.add_argument("--output", default="dummy.csv", help="Path to the output file.")
    parser.add_argument("--size", default=50000, type=int, help="size of output file")
    parser.add_argument("--min_repeat", default=0, type=int, help="min number of repeated element")
    parser.add_argument("--max_repeat", default=3, type=int, help="max number of repeated element")
    
    args = parser.parse_args()  # Parse the command-line arguments
    
    return args      

def main(args):
    df = DataLoader(args.input, min_repeat=args.min_repeat, max_repeat=args.max_repeat, num=args.size).__getitem__()
    df.to_csv(args.output, sep=',', na_rep='NaN')

if __name__ == "__main__":
    args = parse()
    main(args)
