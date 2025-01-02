import re

def find_and_convert_numbers_in_text(text):
    """
    Finds all numbers formatted with commas in the given text and converts them to normal numbers.
    Example: "2,000" -> "2000"
    """
    # Regular expression to find numbers with commas (e.g., 2,000, 20,000)
    pattern = r'\d{1,3}(,\d{3})+'
    
    # Function to remove commas from a matched number
    def remove_commas(match):
        return match.group(0).replace(",", "")
    
    # Replace all matched numbers with their comma-free versions
    return re.sub(pattern, remove_commas, text)

def process_text_file(input_path, output_path, replacements):
    """
    Processes a text file by applying replacements and converting numbers with commas.
    Writes the cleaned text to an output file.
    """
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            TEXT = line.strip()
            if not TEXT:
                continue
            
            # Find and convert numbers with commas in the text
            TEXT = find_and_convert_numbers_in_text(TEXT)
            
            # Apply additional replacements
            for old, new in replacements:
                TEXT = TEXT.replace(old, new)
            
            # Remove extra spaces
            TEXT = re.sub(' +', ' ', TEXT)
            
            # Write the cleaned text to the output file
            outfile.write(TEXT + " ")

replacements = [
    ('VIssịT n0(v)eL/b(i)(n).𝘤𝑜𝓂 for the best novel reading experience', ' '),    ('DiisCoover 𝒖pdated novels on n(o)v./e/lbin(.)co𝒎', ' '),    ('𝑅êạd new chapt𝒆rs on no/v/e/l𝒃in(.)com', ' '),    ('T/his chapter is updat𝓮d by n𝒐v(ê(l)biin.co/m', ' '), ('Gêtt the latest ch𝒂pters on n𝒐/velbin(.)com', ' '), ('Ne/w novel chapt𝒆rs are published on no/vel(/bin(.)co/m', ' '),
    ('Gêtt the latest ch𝒂pters on n𝒐/velbin(.)com', ' '),    ('𝑅êạd new chapt𝒆rs on no/v/e/l𝒃in(.)com', ' '),    ('Fôllôw 𝒏ew stories at n𝒐/v(e)lb/in(.)com', ' '),    ('Findd new 𝒔tories on nov/e(l)bin(.)com', ' '),    ('Finndd the new𝒆st 𝒏ovels on n/𝒐/velbin(.)com', ' '),
    ('Fôll0w current novÊls on n/o/(v)/3l/b((in).(co/m)', ' '),    ('ViiSiit n𝒐velb𝒊/n(.)c/(𝒐)m for l𝒂test 𝒏𝒐vels', ' '),    ('Rêađ lat𝒆st ch𝒂pters on n𝒐/v/𝒆/l(b)i𝒏(.)c𝒐m', ' '),    ('Nnêw n0vel chapters are published on n0v/e/(lb)i(n.)co/m', ' '),    ('Aall 𝒏𝒆west ch𝒂pt𝒆rs on n.o./v𝒆l𝒃i/n/(.)c𝒐m', ' '),    ('Yôur favorite 𝒏ovels at n/𝒐(v)el/bin(.)com', ' '),    ('Fiind upd𝒂ted 𝒏ovels on n𝒐/v/elbin(.)co/m', ' '),
    ('Tôp 𝒏𝒐v𝒆l updates on n/(o)/v/𝒆lb/in(.)com', ' '),    ('𝒩ewW 𝒏ovels upd𝒂tes on nov/𝒆l/b(i)𝒏(.)com', ' '),    ('RêAd lat𝙚St chapters at nô(v)e(l)bin/.c/o/m', ' '),
    ('Gét latest 𝒏ovel ch𝒂pters on n𝒐v(e)lbj/n(.)c/𝒐m', ' '),    ('Fị𝒏dd 𝒏ew upd𝒂t𝒆s on n(o)v/e/l𝒃in(.)com', ' '),    ('DiiScôver 𝒏𝒆w stori𝒆s on no/𝒗/e()/lbin(.)com', ' '),
    ('Alll 𝒍𝒂test nov𝒆l𝒔 on novelb𝒊n/(.)c𝒐m', ' '),    ('Upstodatee from n(0)/v𝒆/lbIn/.(co/m', ' '),    ('nÊw st𝒐ries at n𝒐/vel/b/i/n(.)co𝒎', ' '),
    ('Reêad latest 𝒏ov𝒆ls at n𝒐𝒐v/e/l/bi𝒏(.)com', ' '),    ('Yôur f𝒂vorite stories on 𝒏/o/(v)𝒆/lb𝒊n(.)c𝒐m', ' '),    ('CH𝒆Ck for 𝒏ew st𝒐ries on no/v/el/bin(.)c0m', ' '),    ('Gett your 𝒇avorite 𝒏ovels at no/v/e/lb𝒊n(.)com', ' '),    ('Thê sourc𝗲 of this content n/o/v/(𝒆l)bi((n))', ' '),
    ('Th.ê most uptodat𝓮 n𝒐vels are published on n(0)velbj)n(.)co/m', ' '),    ('Ch𝒆êck out l𝒂t𝒆st 𝒏𝒐v𝒆l𝒔 on nov𝒆l/bin(.)c𝒐m', ' '),    ('Visitt nov𝒆lbin(.)c𝒐/m for the l𝒂test updates', ' '),    ('Diiscover new 𝒔tories at n𝒐ve/lbin(.)c/o𝒎', ' '),
    ('FOlloow 𝒏ewest stories at n𝒐(v)el/bi/n(.)com', ' '),    ('Nêww 𝒄hapters will be fully updated at (n)ov(𝒆)l/bin(.)com', ' '),    ('Gẹtt the l𝒂test 𝒏𝒐v𝒆ls at 𝒏.o/(v)/e/l/bi𝒏(.)co𝒎', ' '),    ('F0lloww new 𝒄hapters at nov/(e)l/bin/(.)com', ' '),
    ('RE𝒂ad updated st𝒐ries at n/𝒐/vel/bin(.)com', ' '),    ('𝒩eew updates 𝒂t n𝒐vel/bi𝒏(.)com', ' '),    ('L𝒂aTest nov𝒆ls on (n)𝒐velbi/𝒏(.)co𝒎', ' '),    ('Follow the latest novels 𝒐𝒏 n𝒐/velbin(.)com', ' '),    ('FiNd 𝒖pd𝒂tes on n(𝒐)/v𝒆l𝒃𝒊n(.)c𝒐m', ' '),    ('Geett the l𝒂test 𝒏𝒐vels on no/v/elbin(.)c/om', ' '),
    ('Expplôre 𝒖ptod𝒂te stories at no/𝒗el//bin(.)c𝒐m', ' '),    ('ÚpTodated 𝒏ov𝒆ls on 𝒏o(v)𝒆l()bin(.)c𝒐m', ' '),    ('Vissit n𝒐velbin(.)c𝒐m for 𝒏ew 𝒏ovels', ' '),
    ('ALL new 𝒄hapters 𝒐n n𝒐v(𝒆)lbin(.)com', ' '),    ('Vissit novelbin(.)c.𝒐m for updates', ' '),    ('Checkk new 𝒏ovel ch𝒂pters at nov𝒆lbin(.)com', ' '),
    ('Upd𝒂ted chapters 𝒐n n𝒐velbin(.)com', ' '),    ('Điscover n𝒆w chapt𝒆rs 𝒐n n0𝒗e(l)bi𝒏(.)com', ' '),    ('Re𝒂𝒂d the latest stories 𝒐n nov𝒆lbin(.)com', ' '),
    ('Visjt n𝒐velbin(.)c𝒐m for new updates', ' '),    ('Explore new 𝒏ovels on n𝒐velbi𝒏(.)com', ' '),    ('Discover 𝒏ew chapters at novelbi𝒏(.)co𝒎', ' '),
    ('Translator: 549690339', ' '),
    ('Translator: 549690339', ' '),
    ("↑Return to top↑", ""),
     (',', ' '), ('.', ','), ('?', ','), ('!', ','),
    ('"', " "), ('\n', ' '),
]

if __name__ == "__main__":
    text_path = 'Text/output'
    process_text_file(text_path + ".txt", text_path + "_replaced.txt", replacements)
