import json
import re
from sv import iv
from sv.models import TSV, Nonreddit
from collections import Counter


class DumpSearcher:
    def __init__(self, paste_text, flag, generation):
        self.incl_nonrdt = flag
        self.gen = generation
        self.max_exceeded = False
        self.MAX_QUERIES_PER_POST = 900
        self.non_rdt_array = []
        self.non_rdt_index = 0
        self.num_of_queries = 0
        self.results_dict_list = []
        self.split_paste_iterable = iter(paste_text.splitlines())
        self.total_egg_matches = 0
        self.user_matches = []
        self.unique_egg_matches = 0

    def process_text(self):
        for line in self.split_paste_iterable:
            if len(line.strip()) != 0:  # skip blank lines
                # parse ESV from KeySAV output
                esv_re_match = re.search('\d\d\d\d', line)
                if self.num_of_queries > self.MAX_QUERIES_PER_POST:
                    max_exceeded = True
                    break
                elif esv_re_match:  # the line contains an ESV
                    esv = esv_re_match.group(0)
                    self.process_line(esv, line)
                else:  # the line does not contain an ESV, so just copy the line
                    no_match = {'copied_str': line,}
                    self.results_dict_list.append(no_match)
        return {'results': self.results_dict_list,
                'gen': self.gen,
                'total': self.total_egg_matches,
                'unique': self.unique_egg_matches,
                'exceeded': self.max_exceeded,
                'multi': self.multiples(self.user_matches),
                'nonreddit': json.dumps(self.non_rdt_array)}

    def process_line(self, esv, line):
        perf = iv.is_perfect(line)
        query_rdt = TSV.objects.tsv_search(esv, self.gen)
        if self.incl_nonrdt:
            query_other = Nonreddit.objects.tsv_search(esv)
        else:
            query_other = None
        self.num_of_queries += 1

        # pass along the string if there are no matches
        if len(query_rdt) == 0 and (query_other is None or len(query_other) == 0):
            self.results_dict_list.append({'copied_str': line, 'iv': perf, 'sv': esv})
        else:
            self.unique_egg_matches += 1
            for i, q in enumerate(query_rdt):
                self.total_egg_matches += 1
                if i == 0:  # first match for an egg->print , dupes->blank
                    dump_output = line
                else:
                    dump_output = ""
                self.user_matches.append(q.trainer.username)  # for multiple matches counter

                flair = self.split_flair(q.trainer.flair_class)

                tbl_row_dict = {'copied_str': dump_output,
                                'username': q.trainer.username,
                                'sub_id': q.sub_id,
                                'sv': esv,
                                'iv': perf,
                                'completed': q.completed,
                                'last_seen': q.last_seen,
                                'pending': q.pending,
                                'main_flair': flair[0],
                                'ribbon_flair': flair[1],
                                'flair_text': q.trainer.flair_text,
                                'archived': q.archived}
                self.results_dict_list.append(tbl_row_dict)

            if self.incl_nonrdt:
                nr_arr = []
                for i, q in enumerate(query_other):
                    if i == 0 and len(query_rdt) == 0:
                        dump_output = line
                    else:
                        dump_output = ""

                    tbl_row_dict = {'copied_str': dump_output,
                                    'source': q['source'],
                                    'sv': esv,
                                    'iv': perf,
                                    'index': self.non_rdt_index,  # used for non-reddit modal to find json array entry
                                    'sub_index': i}
                    self.results_dict_list.append(tbl_row_dict)
                    json_dict = {'username': q['username'],
                                 'tsv': esv,
                                 'url': q['url'],
                                 'fc': q['fc'],
                                 'ign': q['ign'],
                                 'timestamp': q['timestamp'],
                                 'lang': q['language'],
                                 'source': q['source'],
                                 'other': q['other'],
                                 'pkmn': line}
                    nr_arr.append(json_dict)
                if len(nr_arr) > 0:
                    self.non_rdt_array.append(nr_arr)
                    self.non_rdt_index += 1

    def multiples(self, matches): #list of dicts
        matches.sort()
        count = Counter(matches)
        multiple_matches = []
        for k, v in count.items():
            if v > 1:
                multiple_matches.append({'username': k, 'count': v})
        return multiple_matches

    def split_flair(self, full_flair):
        if full_flair == 'default' or full_flair is None:
            return (None, None)
        else:
            split_flair_array = full_flair.split(" ")
            main_flair = split_flair_array[0]
            if main_flair == 'default':
                main_flair = None

            if len(split_flair_array) == 2:
                ribbon_flair = split_flair_array[1]
            else:
                ribbon_flair = None

            return (main_flair, ribbon_flair)
