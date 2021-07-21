#!/usr/bin/python
#########################################################################################
## Author: Pravech Ajawatanawong                                                       ##
## Last Update: 8 JUNE 2021                                                            ##
## Program: SeqFIRE: Sequence Feature and Indel Region Extractor                       ##
## Version: 2.21 (2021)                                                                ##
#########################################################################################
import getopt, sys, os, re, warnings
from math import log10

####################################
##  D E F A U L T    V A L U E S  ##
####################################
amino_acid = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T',\
              'V', 'W', 'X', 'Y', '-']
pMatrices = {'PAM250': [('?'), ('M','I','V','L'), ('D','N','H','Q','E'), ('F','I','L'), ('S','P','A'),\
            ('S','A','G'), ('Q','K','N'), ('R','H','Q'), ('S','T'), ('R','K','Q'), ('S','N'),\
            ('F','W'), ('R','W'), ('G','D')], 'PAM60': [('?'), ('S','A','T'), ('H','N'), ('S','N'),\
            ('N','D'), ('D','E'), ('H','Q'), ('Q','E'), ('Y','F'), ('R','K'), ('M','I'),\
            ('L','M'), ('I','V')], 'BLOSUM40': [('?'), ('S','T'), ('S','A'), ('S','Q','N'),\
            ('H','Y','M'), ('D','E'), ('N','D'), ('H','N'), ('W','Y','F'), ('E','Q','K'),\
            ('K','R'), ('R','Q'), ('L','M','I','V'), ('E','K'), ('A','G'), ('L','F','I'),\
            ('V','T')], 'BLOSUM62': [('?'), ('S','T'), ('S','A'), ('S','N'), ('H','Y'), ('D','E'),\
            ('N','D'), ('H','N'), ('W','Y','F'), ('E','Q','K'), ('K','R','Q'),\
            ('L','M','I','V')], 'BLOSUM80': [('?'), ('Q','R','K'), ('Q','E','K'), ('E','D'), ('D','N'),\
            ('Q','H'), ('Y','H'), ('Y','W'), ('Y','F'), ('S','T'), ('S','A'), ('M','V','L','I')]}
prog_title = '#  SeqFIRE: Sequence Feature and Indel Region Extractor\n#  version 1.0.1 (c) 2011'
infile = 'infile'
analysis_mode = 1
similarity_threshold = 75.0
percent_similarity = 75.0
percent_accept_gap = 40.0
p_matrix = 'NONE'
p_matrix_2 = 'NONE'
inter_indels = 3
twilight = 'True'
partial = 'True'
blocks = 3
strick_combination = 'False'
combine_with_indel = 'False'
fuse = 4
multidata = 1
output_mode = 2

def usage():
	text="""
SeqFIRE: Sequence Feature and Indl Region Extractor
Version 1.0  Copyright 2011
URL: www.seqfire.org
---------------------------------------------------
[ HELP MESSAGE ]

for quick help type
>>> python seqfire.py -h

for quick started just type
>>> python seqfire.py -i {inputfile with path} {other options}

+-------------------+
| Options available |
+-------------------+

Option  Description

 -h     display SeqFIRE help
 -i     path and name of your infile
 -a     analysis module 
             1 = indel region module
             2 = conserved block module
             Default = 1
 -c     similarity threshold for indel regions identification (0.0 - 100.0)
             Default = 75.0
 -d     similarity threshold for conserved blocks identification (0.0 - 100.0) 
             Default = 75.0
 -j     percent accept gap (0.0 - 100.0)
             Default = 40.0
 -g     substitution group for indel identification
             (PAM250, PAM60, BLOSUM40, BLOSUM62, BLOSUM80, or NONE)
             Default = NONE
 -k     substitution group for cnserved block identification
             (PAM250, PAM60, BLOSUM40, BLOSUM62, BLOSUM80, or NONE)
             Default = NONE
 -b     interindel space (1-10)
             Default = 3
 -t     twilight treatment (True or False)
             Default = True
 -p     partial sequence treatment (True or False)
             Default = False
 -s     space between 2 conserved blocks (1, 2, 3, ...)
             Default = 3
 -f     minimum size for non-conserved block (1, 2, 3, ...)
             Default = 4
 -r     strick combination (True or False)
             Default = False
 -e     get indel matrix together with conserved region (True or False)
             Default = False
 -m     multiple data analysis
             1 = single dataset
             2 = multiple datasets (batch mode)
             Default = 2
 -o     output mode
             1 = show output on screen 
             2 = save output in a file
             3 = both show output on screen & save in a file

For more details, please read the SeqFIRE manual (www.seqfire.org/help).
"""
	print (text)

def parseFasta(records):
	rec = []
	seqs = records.split('>')
	del seqs[0]
	for seq in seqs:
		if '\r\n' in records: p = seq.split('\r\n')
		else: p = seq.split('\n')
		if len(p[0]) > 60:
			title = p[0][:60]
		else:
			title = p[0]
		del p[0]
		seq = ''.join("%s" % (k) for k in p)
		rec.append([title, seq.upper()])
	
	title_length = 0
	for r in rec:
		if len(r[0]) > title_length: title_length = len(r[0])
	
	if title_length < 16:
		for r in rec: r[0] = str(r[0]) + ' '*(16 - len(r[0])) + ': '
	else:
		for r in rec: r[0] = str(r[0]) + ' '*(title_length - len(r[0])) + ': '
	return rec

def getGapProfile(seq_lists):
	gap_profile = ''
	for i in range(len(seq_lists[0][1])):
		g = []
		for seq_list in seq_lists:
			g.append(seq_list[1][i])
		if '-' in g:
			gap_profile = gap_profile + '-'
		else:
			gap_profile = gap_profile + 'X'
	#print("Gap profiling complete:\n",gap_profile)
	return gap_profile

#########################################################################
######                                                             ######
######            I N D E L   R E G I O N   M O D U L E            ######
######                                                             ######
#########################################################################

def getBodyAlignmentIndexes(seq_lists):
	gap_profile = getGapProfile(seq_lists)
	ind_n = gap_profile.find('XXXXX')					# Search for N-terminal edge of alignment body
	ind_reverse_c = gap_profile[::-1].find('XXXXX')		# Search for C-terminal edge of alignment body
	ind_c = len(gap_profile) - ind_reverse_c - 1
	return [ind_n, ind_c]

def getBodyOfAlignment(ind, seq_lists):
	body_alignment = []
	for seq_list in seq_lists:
		record = []
		title = seq_list[0]
		seq = seq_list[1][ind[0]:ind[1]+1]
		record = [title, seq]
		body_alignment.append(record)
	return body_alignment

def genMaskRef(seq_lists, position):
	ref = ''
	for i in range(0, position, 1):
		count = 0
		for seq_list in seq_lists:
			if not seq_list[1][i] == '-': count += 1
		if float(count)/float(len(seq_lists))*100.0 >= 55.0: ref = ref + '?'
		else: ref = ref + '-'
	return ref

def getNRaggedRegion(n_position, seq_lists):
	n_ragged = []
	if partial == 'True':
		if n_position <= 3:
			for seq_list in seq_lists:
				seq = '?' * n_position
				n_ragged.append([seq_list[0], seq])
		else:
			maskRef = genMaskRef(seq_lists, n_position)
			if '?' in maskRef:
				for seq_list in seq_lists:
					rec = []
					if not seq_list[1].startswith('-'):
						n_ragged.append([seq_list[0], seq_list[1][:n_position]])
					elif seq_list[1][:n_position].count('-') == n_position:
						n_ragged.append([seq_list[0], maskRef])
					else:
						m = re.search(r'-[ACDEFGHIKLMNPQRSTVWXY]', str(seq_list[1][:n_position]))
						try:
							n = m.start() + 1
						except:
							n = 0
						n_ragged.append([seq_list[0], maskRef[:n] + seq_list[1][n:n_position]])
	elif partial == 'False':
		for seq_list in seq_lists:
			seq = '?' * n_position
			n_ragged.append([seq_list[0], seq])
	return n_ragged

def getCRaggedRegion(c_position, seq_lists):
	c_ragged = []
	if partial == 'True':
		if len(seq_lists[0][1])-c_position <= 3:
			for seq_list in seq_lists:
				seq = '?' * (len(seq_list[1]) - c_position - 1)
				c_ragged.append([seq_list[0], seq])
		else:
			new_seq_lists = []
			for seq_list in seq_lists:
				a = [seq_list[0], seq_list[1][::-1]]
				new_seq_lists.append(a)
			inv_maskRef = genMaskRef(new_seq_lists, len(new_seq_lists[0][1])-c_position-1)
			if '?' in inv_maskRef:
				for seq_list in seq_lists:
					rec = []
					if not seq_list[1].endswith('-'):
						c_ragged.append([seq_list[0], seq_list[1][c_position+1:]])
					elif seq_list[1][c_position+1:].count('-') == len(seq_list[1])-c_position-1:
						c_ragged.append([seq_list[0], inv_maskRef[::-1]])
					else:
						m = re.search(r'-[ACDEFGHIKLMNPQRSTVWXY]', str(seq_list[1][::-1]))
						try:
							n = m.start() + 1
						except:
							n = 0
						rec = [seq_list[0], str(seq_list[1][c_position+1:len(seq_list[1])-n]) + str(inv_maskRef[n-1::-1])]
						c_ragged.append(rec)
	elif partial == 'False':
		for seq_list in seq_lists:
			seq = '?' * (len(seq_list[1]) - c_position - 1)
			c_ragged.append([seq_list[0], seq])
	return c_ragged

def genPseudoalignment(seq_lists):
	p, pseudoalignment = [], []
	ragged_positions = getBodyAlignmentIndexes(seq_lists)
	body_of_alignment = getBodyOfAlignment(ragged_positions, seq_lists)

	# GENERATES THE N-TERMINAL RAGGED
	n_ragged_alignment = getNRaggedRegion(ragged_positions[0], seq_lists)

	# GENERATES THE C-TERMINAL RAGGED
	c_ragged_alignment = getCRaggedRegion(ragged_positions[1], seq_lists)

	# COMBINATION OF N-TERMINAL RAGGED, BODY OF ALIGNMENT AND C-TERMINAL RAGGED
	for k in range(0, len(body_of_alignment), 1):
		seq = [body_of_alignment[k][0], n_ragged_alignment[k][1] + body_of_alignment[k][1] + c_ragged_alignment[k][1]]
		pseudoalignment.append(seq)
	return pseudoalignment

def getSimilarityScore(aa):
	if p_matrix == 'NONE':
		aa_dict = {'A': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0,\
		            'K': 0, 'L': 0, 'M': 0, 'N': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0,\
		            'T': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, '?': 0}
		for a in aa:
			aa_dict[a] = aa_dict[a] + 1
		k = max(aa_dict, key=aa_dict.get)
		similarity = (float(aa_dict[k]) * 100.0) / float(len(aa))
		if twilight == 'True':
			if similarity >= 30.0: return 'C'
			else: return '.'
		elif twilight == 'False':
			if similarity >= similarity_threshold: return 'C'
			else: return '.'
	else:
		pMatrix = pMatrices[p_matrix]
		c = []
		aa_dict = {'A': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0,\
		            'K': 0, 'L': 0, 'M': 0, 'N': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0,\
		            'T': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, '?': 0}
		for a in aa: aa_dict[a] = aa_dict[a] + 1
		for aa_sets in pMatrix:
			m = 0
			for aa_set in aa_sets: m = m + int(aa_dict[aa_set])
			c.append((float(m)*100.0)/float(len(aa)))
		similarity = max(c)
		if twilight == 'True':
			if similarity >= 30.0: return 'C'
			else: return '.'
		elif twilight == 'False':
			if similarity >= similarity_threshold: return 'C'
			else: return '.'

def getConservedBlockProfile(pseudoSeq_lists):
	consBlkProfile = ''
	gapProfile = getGapProfile(pseudoSeq_lists)
	for i in range(0, len(gapProfile), 1):
		if gapProfile[i] == '-':
			consBlkProfile = consBlkProfile + '-'
		else:
			aa = []
			for pseudoSeq_list in pseudoSeq_lists:
				aa.append(pseudoSeq_list[1][i])
			ans = getSimilarityScore(aa)
			consBlkProfile = consBlkProfile + ans
	return consBlkProfile

def getIndelProfile(conserved_block_profile):
	while (conserved_block_profile.count('-.')+conserved_block_profile.count('.-')>0):
		conserved_block_profile = conserved_block_profile.replace('-.', '--')
		conserved_block_profile = conserved_block_profile.replace('.-', '--')
	conserved_block_profile = conserved_block_profile.replace('.', 'C')

	for i in range(inter_indels-1, 0, -1):
		conserved_block_profile = conserved_block_profile.replace('-'+'C'*i+'-', '-'*(i+2))
	m = re.search('C', conserved_block_profile)
	start_point = m.start()
	m = re.search('C', conserved_block_profile[::-1])
	end_point = len(conserved_block_profile) - (m.end() - 1)

	sub_conserved_block_profile = conserved_block_profile[start_point:end_point]
	sub_conserved_block_profile = sub_conserved_block_profile.replace('-', 'I')
	sub_conserved_block_profile = sub_conserved_block_profile.replace('C', '.')
	return '.'*start_point + sub_conserved_block_profile + '.' * (len(conserved_block_profile) - end_point)

def getIndelPositions(indel_profile):
	indel_position = []
	for i in range(0, len(indel_profile)-1, 1):
		current_position = indel_profile[i]
		next_position = indel_profile[i+1]
		if current_position == '.' and next_position == 'I': indel_position.append(i+1)
		elif current_position == 'I' and next_position == '.': indel_position.append(i+1)
	return indel_position

def getRuler(title_length, seq_length):
	scale_of_10 = '---------|'
	ruler = ' ' * title_length
	for i in  range(50, seq_length, 50):
		ruler = ruler + ' ' * (50 - len(str(i))) + str(i)
	scale = ' ' * title_length + scale_of_10 * (seq_length//10) + scale_of_10[0:seq_length % 10]
	return ruler + '\n' + scale

def genIndelAlignment(seq_lists, indel_profile, ruler, indel_positions):
	output_indel_1 = []
	heading = '%s\n#  OUTPUT: ANNOTATED ALIGNMENT\n#  There are %s indels found.\n' % (prog_title, len(indel_positions)//2)
	output_indel_1.append(heading)
	output_indel_1.append(ruler)
	for seq_list in seq_lists:
		line = seq_list[0] + seq_list[1]
		output_indel_1.append(line)
	indelRef_line = ' '*len(seq_lists[0][0]) + indel_profile
	output_indel_1.append(indelRef_line)
	return output_indel_1 

def genHomologAlignment(seq_lists, indel_profile, ruler, indel_positions):
	output_indel_4 = []
	masked_alignment = []
	homolog_positions = []

	g = getBodyAlignmentIndexes(seq_lists)
	homolog_positions.append(g[0])
	for j in indel_positions: homolog_positions.append(j)
	homolog_positions.append(g[1])

	for seq_list in seq_lists:
		new_seq = ''
		for i in range(0, len(homolog_positions), 2):
			new_seq = new_seq + seq_list[1][homolog_positions[i]:homolog_positions[i+1]]
		masked_alignment.append([seq_list[0], new_seq])
	
	heading = '''#NEXUS
	 			 BEGIN DATA;
				 \tDIMENSIONS NTAX=%s NCHAR=%s;
				 \tFORMAT MISSING=? DATATYPE=PROTEIN GAP=-;
				 \tOPTIONS GAPMODE=MISSING;


				 MATRIX''' % (len(masked_alignment), len(masked_alignment[0][1]))
	output_indel_4.append(heading)
	#ruler = getRuler(len(masked_alignment[0][0]), len(masked_alignment[0][1]))

	r = getRuler(len(masked_alignment[0][0]), len(masked_alignment[0][1])).split('\n')
	ruler = '[' + r[0][1:] + ' '*(len(r[1])-len(r[0])) + ']\n[' + r[1][1:] + ']'


	output_indel_4.append(ruler)

	for s in masked_alignment:
		line = s[0] + s[1]
		output_indel_4.append(line)
	line = 'END;'
	output_indel_4.append(line)
	return output_indel_4 

def search_for_simple_indels(pseudoalignments, inter_indels, indel_positions):
	indels = ''
	for i in range(0, len(indel_positions), 2):
		simple = True
		for pseudoalignment in pseudoalignments:
			indel_body = pseudoalignment[1][indel_positions[i]:indel_positions[i+1]]
			if not ('-'*len(indel_body) == indel_body or not '-' in indel_body): 
				simple = False
		if simple: indels = indels + 's'
		else: indels = indels + 'c'
	return indels

def genIndelLists(pseudoalignments, inter_indels, indel_positions, simple_indel_positions):
	output_indel_2 = []
	heading = '%s\n#  OUTPUT: INDEL LIST\n#  There are %s indels found.\n#  ** indicates masked sequence\n' % (prog_title, len(indel_positions)//2)
	output_indel_2.append(heading)
	id = 1
	for i in range(0, len(indel_positions), 2):
		if simple_indel_positions[id-1] == 's': indel_type = 'simple indel'
		elif simple_indel_positions[id-1] == 'c': indel_type = 'complex indel'

		if indel_positions[i] + 1 == indel_positions[i+1]:
			line = '//\nIndel number: ' + str(id) + '\nIndel location in alignment: ' + str(indel_positions[i] + 1) + '\nSize of indel: ' +\
				    str(indel_positions[i+1] - indel_positions[i]) + ' alignment columns\nType: ' + indel_type + '\n'
		else:
			line = '//\nIndel number: ' + str(id) + '\nIndel location in alignment: ' + str(indel_positions[i] + 1) + '-' +\
				    str(indel_positions[i+1]) + '\nSize of indel: ' + str(indel_positions[i+1] - indel_positions[i]) +\
				    ' alignment columns\nType: ' + indel_type + '\n'
		for pseudoalignment in pseudoalignments:
			upstream_region = pseudoalignment[0] + pseudoalignment[1][indel_positions[i]-inter_indels:indel_positions[i]]
			indel_body = pseudoalignment[1][indel_positions[i]:indel_positions[i+1]]
			downstream_region = pseudoalignment[1][indel_positions[i+1]:indel_positions[i+1]+inter_indels]
			if '?' in upstream_region or '?' in indel_body or '?' in downstream_region:
				line = line + '\n' + upstream_region + '  ' + indel_body + '  ' + downstream_region + '  **'
			else:
				line = line + '\n' + upstream_region + '  ' + indel_body + '  ' + downstream_region
		output_indel_2.append(line)
		id += 1
	return output_indel_2

def getIndelMatrix(output_indel_2, simple_indel_positions, indel_positions):
	output_indel_3 = []
	output_indel_2 = ''.join(output_indel_2)
	records = output_indel_2.split('//')
	del records[0]

	### Title manipulation
	titles = []
	ls = records[0].split('\n')	
	for i in range(6, len(ls), 1):
		a = ls[i].split(': ')
		titles.append(a[0]+': ')

	arr, i_details = [], []
	for j in range(0, len(simple_indel_positions), 1):
		dat = []
		if simple_indel_positions[j] == 's':
			lines = records[j].split('\n')
			a = lines[1].split(': ')
			no_of_indel = a[1]
			a = lines[2].split(': ')
			indel_location = a[1]
			a = lines[3].split(': ')
			b = a[1].split(' ')
			inde_size = b[0]
			del lines[:6]
			dat = [no_of_indel, indel_location, inde_size]
			i_details.append(dat)
			row = []
			for line in lines:
				a = line.split(': ')
				seq = a[1].split('  ')
				if '-'*len(seq[1]) == seq[1]:
					row.append('0')
				elif not '-' in seq[1]:
					row.append('1')
			arr.append(row)
	arr = [[r[col] for r in arr] for col in range(len(arr[0]))]

	heading = '#NEXUS\nBEGIN DATA;\n    DIMENSION NTAX=%s NCHAR=%s;\
			   \n    FORMAT DATATYPE=SYMBOL "0 1";\
			   \n    OPTIONS GAPMODE=MISSING;\n\nMATRIX' % (len(arr), len(arr[0]))
	output_indel_3.append(heading)
	r = getRuler(len(titles[0]), len(arr[0])).split('\n')
	ruler = '[' + r[0][1:] + ' '*(len(r[1])-len(r[0])) + ']\n[' + r[1][1:] + ']'
	output_indel_3.append(ruler)

	for k in range(0, len(titles), 1):
		line = titles[k] + str(''.join(arr[k]))
		output_indel_3.append(line)

	h1 = ';\nEND;\n\nBEGIN NOTES;\n[ Indel Number     Alignment Position      Indel Length ]\
		  \n[ ------------     ------------------      ------------ ]'
	output_indel_3.append(h1)

	for i_detail in i_details:
		line = '[    ' + i_detail[0] + ' '*(17-len(i_detail[0])) + i_detail[1] +\
			   ' '*(24-len(i_detail[1])) + i_detail[2] + ' '*(10-len(i_detail[2])) + ']'
		output_indel_3.append(line)
	output_indel_3.append('\nEND;')
	return output_indel_3

def getIndelCharacter(output_indel_2, simple_indel_positions, indel_positions):
	output_indel_3 = []
	output_indel_2 = ''.join(output_indel_2)
	records = output_indel_2.split('//')
	del records[0]

	arr, i_details = [], []
	for j in range(0, len(simple_indel_positions), 1):
		dat = []
		if simple_indel_positions[j] == 's':
			lines = records[j].split('\n')
			a = lines[1].split(': ')
			no_of_indel = a[1]
			a = lines[2].split(': ')
			indel_location = a[1]
			a = lines[3].split(': ')
			b = a[1].split(' ')
			inde_size = b[0]
			del lines[:6]
			dat = [no_of_indel, indel_location, inde_size]
			i_details.append(dat)
			row = []
			for line in lines:
				a = line.split(': ')
				seq = a[1].split('  ')
				if '-'*len(seq[1]) == seq[1]:
					row.append('0')
				elif not '-' in seq[1]:
					row.append('1')
			arr.append(row)
	return [[r[col] for r in arr] for col in range(len(arr[0]))]

def indelExtraction(handle):
	pseudoalignments = genPseudoalignment(handle)
	#print("Pseudo alignments:")
	#for onepalign in pseudoalignments:
    #		print(onepalign)
	conserved_block_profile = getConservedBlockProfile(pseudoalignments)
	#print("Conserved block profile:\n",conserved_block_profile)
	indel_profile = getIndelProfile(conserved_block_profile)
	#print("Indel profile:\n",indel_profile)
	indel_positions = getIndelPositions(indel_profile)
	#print("Indel positions:\n",indel_positions)
	ruler = getRuler(len(handle[0][0]), len(handle[0][1]))

	######################
	##  OUTPUT Section  ##
	######################

	if partial == 'True':
		output_indel_1 = genIndelAlignment(pseudoalignments, indel_profile, ruler, indel_positions)
		#output_indel_4 = genHomologAlignment(pseudoalignments, indel_profile, ruler, indel_positions)
	elif partial == 'False':
		output_indel_1 = genIndelAlignment(handle, indel_profile, ruler, indel_positions)
		#output_indel_4 = genHomologAlignment(handle, indel_profile, ruler, indel_positions)

	output_indel_4 = genHomologAlignment(handle, indel_profile, ruler, indel_positions)

	simple_indel_positions = search_for_simple_indels(pseudoalignments, inter_indels, indel_positions)
	output_indel_2 = genIndelLists(pseudoalignments, inter_indels, indel_positions, simple_indel_positions)

	if 's' in simple_indel_positions:
		output_indel_3 = getIndelMatrix(output_indel_2, simple_indel_positions, indel_positions)
	else:
		output_indel_3 = ['###################\n###  NO MATRIX  ###\n###################',\
		'SeqFIRE cannot generate indel matrix because there is no simple indel in the alignment!!']
		
	filename = os.path.basename(infile).split('.')

	if output_mode == 1 or output_mode == 3:
		for out1 in output_indel_1: print (out1)
		print ('\n---SeqFIRE---\n')
		for out2 in output_indel_2: print (out2)
		print ('\n---SeqFIRE---\n')
		for out3 in output_indel_3: print (out3)
		print ('\n---SeqFIRE---\n')
		for out4 in output_indel_4: print (out4)
	if output_mode == 2 or output_mode == 3:
		### Writing output1: Alignment with Indel Mask
		f1 = open(r'%s.txt' % (filename[0]), 'w')
		f1.write(output_indel_1[0])
		f1.write(output_indel_1[1] + '\n')
		del output_indel_1[:2]
		for out1 in output_indel_1: f1.write(str(out1) + '\n')
		f1.close()

		### Writing output2: Indel List
		f2 = open(r'%s.indel' % (filename[0]), 'w')
		f2.write(output_indel_2[0])
		del output_indel_2[0]
		for out2 in output_indel_2: f2.write('\n' + str(out2))
		f2.close()

		### Writing output3: Indel Matrix
		f3 = open(r'%s_matrix.nex' % (filename[0]), 'w')
		for out3 in output_indel_3: f3.write('\n' + str(out3))		
		f3.close()

		### Writing output4: Msked Alignment
		f4 = open(r'%s.nex' % (filename[0]), 'w')
		for out4 in output_indel_4: f4.write('\n' + str(out4))		
		f4.close()

#########################################################################
######                                                             ######
######         C O N S E R V E D   B L O C K   M O D U L E         ######
######                                                             ######
#########################################################################

def getListOfSimilarityScores(handle):
	similarityList = []
	for i in range(0, len(handle[0][1]), 1):
		aa_dict = {'A': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0,\
		            'K': 0, 'L': 0, 'M': 0, 'N': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0,\
		            'T': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, '-': 0, '?': 0}
		for seq_list in handle:
			aa_dict[seq_list[1][i]] += 1

		if p_matrix_2 == 'NONE':
			if (float(aa_dict['-']) * 100.0) / float(len(handle)) >= percent_accept_gap:
				similarityList.append('-')
			else:
				k = max(aa_dict, key=aa_dict.get)
				similarityList.append((float(aa_dict[k]) * 100.0) / float(len(handle)))
		else:
			pMatrix = pMatrices[p_matrix_2]
			if (float(aa_dict['-']) * 100.0) / float(len(handle)) >= percent_accept_gap:
				similarityList.append('-')
			else:
				c = []
				for aa_sets in pMatrix:
					m = 0
					for aa_set in aa_sets: m = m + int(aa_dict[aa_set])
					c.append((float(m)*100.0)/float(len(handle)))
				similarityList.append(max(c))
	return similarityList
		
def getSimilarityProfile(similarity_list):
	similarityProfile = ''
	for i in similarity_list:
		if i == '-':
			similarityProfile = similarityProfile + i
		elif i >= percent_similarity:
			similarityProfile = similarityProfile + 'H'
		elif i < percent_similarity:
			similarityProfile = similarityProfile + '.'
	return similarityProfile

def getSimilarityBlocks(similarity_profile):
	similarityBlocks = similarity_profile
	for i in range(blocks, 0, -1):
		pattern = 'H' + '.'*i + 'H'
		replaceWith = 'H' + 'H'*i + 'H'
		while pattern in similarityBlocks:
			similarityBlocks = similarityBlocks.replace(pattern, replaceWith)

	for j in range(1, fuse+1, 1):
		pattern = '.' + 'H'*j + '.'
		replaceWith = '.' + '.'*j + '.'
		while pattern in similarityBlocks:
			similarityBlocks = similarityBlocks.replace(pattern, replaceWith)

		pattern = '.' + 'H'*j + '-'
		replaceWith = '.' + '.'*j + '-'
		while pattern in similarityBlocks:
			similarityBlocks = similarityBlocks.replace(pattern, replaceWith)

		pattern = '-' + 'H'*j + '.'
		replaceWith = '-' + '.'*j + '.'
		while pattern in similarityBlocks:
			similarityBlocks = similarityBlocks.replace(pattern, replaceWith)

		pattern = '-' + 'H'*j + '-'
		replaceWith = '-' + '.'*j + '-'
		while pattern in similarityBlocks:
			similarityBlocks = similarityBlocks.replace(pattern, replaceWith)
	return similarityBlocks

def getInformationEntropy(handle):
	entropyList = []
	for i in range(0, len(handle[0][1]), 1):
		aa_dict = {'A': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0,\
		            'K': 0, 'L': 0, 'M': 0, 'N': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0,\
		            'T': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, '-': 0, '?': 0}
		for seq_list in handle:
			aa_dict[seq_list[1][i]] += 1

		if (float(aa_dict['-']) * 100.0) / float(len(handle)) >= percent_accept_gap:
			entropyList.append('-')
		else:
			site_entropy = 0.0
			for aa in amino_acid:
				proportion_of_any_amino_acid = float(aa_dict[aa])/float(len(handle))
				if not proportion_of_any_amino_acid == 0.0:
					site_entropy = site_entropy + (proportion_of_any_amino_acid * log10(proportion_of_any_amino_acid))
					site_entropy = site_entropy * (-1.0)
			entropyList.append(site_entropy)
	return entropyList

def getMedian(numericValues):
	theValues = sorted(numericValues)
	if len(theValues) % 2 == 1:
		return theValues[(len(theValues)+1)//2-1]
	else:
		lower = theValues[len(theValues)//2-1]
		upper = theValues[len(theValues)//2]
	return (float(lower + upper)) / 2  

def getEntropyProfile(entropy_list):
	datalists = []
	for i in entropy_list:
		if not i == '-': datalists.append(i)
	median = getMedian(datalists)

	entropyProfile = ''
	for i in entropy_list:
		if i == '-': entropyProfile = entropyProfile + '-'
		elif i >= median*1.4826: entropyProfile = entropyProfile + '.'
		elif i < median*1.4826: entropyProfile = entropyProfile + 'E'
		#elif i >= median*1.4826 or i <= median*(-1.4826): entropyProfile = entropyProfile + '.'
		#elif i < median*1.4826 and i > median*(-1.4826): entropyProfile = entropyProfile + 'E'
	return entropyProfile

def getEntropyBlocks(entropy_profile):
	entropyBlocks = entropy_profile
	for i in range(blocks, 0, -1):
		pattern = 'E' + '.'*i + 'E'
		replaceWith = 'E' + 'E'*i + 'E'
		while pattern in entropyBlocks:
			entropyBlocks = entropyBlocks.replace(pattern, replaceWith)

	for j in range(1, fuse+1, 1):
		pattern = '.' + 'E'*j + '.'
		replaceWith = '.' + '.'*j + '.'
		while pattern in entropyBlocks:
			entropyBlocks = entropyBlocks.replace(pattern, replaceWith)

		pattern = '.' + 'E'*j + '-'
		replaceWith = '.' + '.'*j + '-'
		while pattern in entropyBlocks:
			entropyBlocks = entropyBlocks.replace(pattern, replaceWith)

		pattern = '-' + 'E'*j + '.'
		replaceWith = '-' + '.'*j + '.'
		while pattern in entropyBlocks:
			entropyBlocks = entropyBlocks.replace(pattern, replaceWith)

		pattern = '-' + 'E'*j + '-'
		replaceWith = '-' + '.'*j + '-'
		while pattern in entropyBlocks:
			entropyBlocks = entropyBlocks.replace(pattern, replaceWith)
	return entropyBlocks

def searchForConservedBlocks(similarity_blocks, entropy_blocks):
	conservedBlocks = ''
	if strick_combination == 'True':
		for i in range(0, len(similarity_blocks), 1):
			if similarity_blocks[i] == '-' and entropy_blocks[i] == '-':
				conservedBlocks = conservedBlocks + '-'
			elif similarity_blocks[i] == 'H' and entropy_blocks[i] == 'E':
				conservedBlocks = conservedBlocks + '#'
			else:
				conservedBlocks = conservedBlocks + '.'
	elif strick_combination == 'False':
		for i in range(0, len(similarity_blocks), 1):
			if similarity_blocks[i] == '-' and entropy_blocks[i] == '-':
				conservedBlocks = conservedBlocks + '-'
			elif similarity_blocks[i] == 'H' or entropy_blocks[i] == 'E':
				conservedBlocks = conservedBlocks + '#'
			else:
				conservedBlocks = conservedBlocks + '.'
	return conservedBlocks

def genConservedAlignment(handle, conserved_blocks, ruler, indel_profile):
	output_conserved_1 = []
	heading = '%s\n#  OUTPUT: PROTEIN ALIGNMENT WITH CONSERVED BLOCK PROFILE\n#  NOTE: # in the reference line means conserved block positions.\n' % (prog_title)
	output_conserved_1.append(heading)
	output_conserved_1.append(ruler)
	for i in handle:
		line = i[0] + i[1]
		output_conserved_1.append(line)
	line = 'Conserved Blocks' + ' ' * (len(handle[0][0])-16) + conserved_blocks
	output_conserved_1.append(line)
	if indel_profile == '':
		pass
	else:
		line = 'Indel Profile   ' + ' ' * (len(handle[0][0])-16) + indel_profile
		output_conserved_1.append(line)
	return output_conserved_1

def genFastaWithConservedProfile(handle, conserved_blocks):
	output_conserved_2 = []
	for record in handle:
		output_conserved_2.append('>' + record[0][:-2])
		output_conserved_2.append(record[1])
	output_conserved_2.append('>Conserved blocks')
	output_conserved_2.append(conserved_blocks)
	return output_conserved_2

def genFastaWithConservedBlockOnly(handle, conserved_blocks):
	output_conserved_3, conserved_index = [], []

	# Find the conserved block positions
	ref = '-' + conserved_blocks + '-'
	for i in range(0, len(ref)-1, 1):
		current_position = ref[i]
		next_position = ref[i+1]
		if not current_position == '#' and next_position == '#': conserved_index.append(i)
		elif current_position == '#' and not next_position == '#': conserved_index.append(i)

	for record in handle:
		output_conserved_3.append('>' + record[0][:-2])
		seq = ''
		for i in range(0, len(conserved_index), 2):
			seq = seq + record[1][conserved_index[i]:conserved_index[i+1]]
		output_conserved_3.append(seq)
	return output_conserved_3

def genNexusWithConservedProfile(handle, conserved_blocks, simple_indel_positions, indel_positions, indel_profile):
	output_conserved_4 = []
	conserved_index = []
	charset = '     charset conRes ='
	
	# Prepare conRes
	ref = '-' + conserved_blocks + '-'
	for i in range(0, len(ref)-1, 1):
		current_position = ref[i]
		next_position = ref[i+1]
		if not current_position == '#' and next_position == '#': conserved_index.append(i)
		elif current_position == '#' and not next_position == '#': conserved_index.append(i)

	for i in range(0, len(conserved_index), 2):
		charset = charset + ' ' + str(conserved_index[i]+1) + '-' + str(conserved_index[i+1])


	head = '''#NEXUS
	 		BEGIN DATA;
			\tDIMENSIONS NTAX=%s NCHAR=%s;
 		    \tFORMAT MISSING=? DATATYPE=PROTEIN GAP=- EQUATE="0=K 1=D";
 		    \tOPTIONS GAPMODE=MISSING;
			 

			 MATRIX''' % (len(handle),len(handle[0][1]))
	output_conserved_4.append(head)

	r = getRuler(len(handle[0][0]), len(handle[0][1])).split('\n')
	ruler = '[ ' + r[0][1:] + ' '*(len(r[1])-len(r[0])) + ']\n[ ' + r[1][1:] + ']'
	output_conserved_4.append(ruler)
	for i in handle:
		line = i[0] + ' ' + i[1]
		output_conserved_4.append(line)
	line = '[Conserved Block Profile' + ' ' * (len(handle[0][0])-23) + conserved_blocks + ']'
	output_conserved_4.append(line)

	indelChar = ''
	for j in range(0, len(indel_positions), 2):
		indelChar = indelChar + ' ' + str(indel_positions[j]) + '-' + str(indel_positions[j+1])

	if combine_with_indel == 'True':
		line = '[Indel profile' + ' ' * (len(handle[0][0])-13) + indel_profile + ']'
		output_conserved_4.append(line)
		line = ';\nEND;\n\nBEGIN SETS;'
		output_conserved_4.append(line)		
		charset = charset + ';\n     charset indels =' + indelChar
		charset = charset + ';\n     charset indelMatrix = ' + str(len(handle[0][1])-simple_indel_positions.count('s')+1) + '-' + str(len(handle[0][1]))	+ ';\nEND;'
		output_conserved_4.append(charset)
		#line = '\nBEGIN CHARACTER;\n     eliminate '
		#output_conserved_4.append(line)		
		h1 = 'END;\n\nBEGIN NOTES;\n[ Indel Number     Alignment Position      Indel Length ]\n[ ------------     ------------------      ------------ ]'
		output_conserved_4.append(h1)
		for i, status in enumerate(simple_indel_positions):
			if status == 's':
				if indel_positions[0]+1 == indel_positions[1]:
					align_pos = str(indel_positions[0]+1)
				else:
					align_pos = str(indel_positions[0]+1) + '-' + str(indel_positions[1])
				indel_length = indel_positions[1] - indel_positions[0]
				line = '[     ' + str(i+1) + ' '*(17-len(str(i+1))) + align_pos + ' '*(24-len(align_pos)) + str(indel_length) + ' '*(9-len(str(indel_length))) + ']'
				output_conserved_4.append(line)
				del indel_positions[0:2]
			elif status == 'c':
				del indel_positions[0:2]
		output_conserved_4.append('\nEND;')
	elif combine_with_indel == 'False':
		line = ';\nEND;\n\nBEGIN SETS;'
		output_conserved_4.append(line)		
		charset = charset + ';\n     charset indels =' + indelChar + ';\nEND;'
		output_conserved_4.append(charset)
		#line = '\n\nBEGIN CHARACTER;\n     eliminate '
		#output_conserved_4.append(line)		
		#line = 'END;'
		#output_conserved_4.append(line)		
	return output_conserved_4

def genNexusWithConservedBlockOnly(output_conserved_3):
	output_conserved_5 = []

	head = '#NEXUS\nBEGIN DATA;\n     DIMENSIONS NTAX=%s NCHAR=%s;\
 		    \n     FORMAT MISSING=? DATATYPE=PROTEIN GAP=- EQUATE="0=K 1=D";\
 		    \n     OPTIONS GAPMODE=MISSING;\n\nMATRIX' % (len(output_conserved_3)//2, len(output_conserved_3[1]))
	output_conserved_5.append(head)
	
	r = getRuler(len(output_conserved_3[0]), len(output_conserved_3[1])).split('\n')
	ruler = '[ ' + r[0][1:] + ' '*(len(r[1])-len(r[0])) + ']\n[ ' + r[1][1:] + ']'
	output_conserved_5.append(ruler)
	
	for i in range(0, len(output_conserved_3), 2):
		line = output_conserved_3[i][1:] + ': ' + output_conserved_3[i+1]
		output_conserved_5.append(line)

	line = ';\nEND;'
	output_conserved_5.append(line)		
	return output_conserved_5

def conservedBlockExtraction(handle):
	similarity_list = getListOfSimilarityScores(handle)
	similarity_profile = getSimilarityProfile(similarity_list)
	similarity_blocks = getSimilarityBlocks(similarity_profile)
	entropy_list = getInformationEntropy(handle)
	entropy_profile = getEntropyProfile(entropy_list)
	entropy_blocks = getEntropyBlocks(entropy_profile)
	conserved_blocks = searchForConservedBlocks(similarity_blocks, entropy_blocks)

	############################################
	##     Extraction of Conserved Blocks     ##
	############################################

	if combine_with_indel == 'True':
		pseudoalignments = genPseudoalignment(handle)
		conserved_block_profile = getConservedBlockProfile(pseudoalignments)
		indel_profile = getIndelProfile(conserved_block_profile)
		indel_positions = getIndelPositions(indel_profile)

		simple_indel_positions = search_for_simple_indels(pseudoalignments, inter_indels, indel_positions)
		output_indel_2 = genIndelLists(pseudoalignments, inter_indels, indel_positions, simple_indel_positions)
		if 's' in simple_indel_positions:
			indel_in_matrix = getIndelCharacter(output_indel_2, simple_indel_positions, indel_positions)
			for i in range(0, len(indel_in_matrix), 1):
				handle[i][1] = handle[i][1] + ''.join(indel_in_matrix[i])
		ruler = getRuler(len(handle[0][0]), len(handle[0][1]))
		output_conserved_1 = genConservedAlignment(handle, conserved_blocks, ruler, indel_profile)
		output_conserved_2 = genFastaWithConservedProfile(handle, conserved_blocks)
		output_conserved_3 = genFastaWithConservedBlockOnly(handle, conserved_blocks)
		output_conserved_4 = genNexusWithConservedProfile(handle, conserved_blocks, simple_indel_positions, indel_positions, indel_profile)
		output_conserved_5 = genNexusWithConservedBlockOnly(output_conserved_3)
	elif combine_with_indel == 'False':
		pseudoalignments = genPseudoalignment(handle)
		conserved_block_profile = getConservedBlockProfile(pseudoalignments)
		indel_profile = getIndelProfile(conserved_block_profile)
		indel_positions = getIndelPositions(indel_profile)

		ruler = getRuler(len(handle[0][0]), len(handle[0][1]))
		output_conserved_1 = genConservedAlignment(handle, conserved_blocks, ruler, '')
		output_conserved_2 = genFastaWithConservedProfile(handle, conserved_blocks)
		output_conserved_3 = genFastaWithConservedBlockOnly(handle, conserved_blocks)
		output_conserved_4 = genNexusWithConservedProfile(handle, conserved_blocks, '', indel_positions, '')
		output_conserved_5 = genNexusWithConservedBlockOnly(output_conserved_3)
	
	######################
	##  OUTPUT Section  ##
	######################

	filename = os.path.basename(infile).split('.')

	if output_mode == 1 or output_mode == 3:
		for out1 in output_conserved_1: print (out1)
		print ('\n---SeqFIRE---\n')
		for out2 in output_conserved_2: print (out2)
		print ('\n---SeqFIRE---\n')
		for out3 in output_conserved_3: print (out3)
		print ('\n---SeqFIRE---\n')
		for out4 in output_conserved_4: print (out4)
		print ('\n---SeqFIRE---\n')
		for out5 in output_conserved_5: print (out5)
	if output_mode == 2 or output_mode == 3:
		### Writing output1: Alignment with Indel Mask
		f1 = open(r'%s.txt' % (filename[0]), 'w')
		f1.write(output_conserved_1[0])
		f1.write(output_conserved_1[1] + '\n')
		del output_conserved_1[:2]
		for out1 in output_conserved_1: f1.write(str(out1) + '\n')
		f1.close()
		### Writing output2: Alignment in Fasta format + Conserved block profile
		f2 = open(r'%s.fasta' % (filename[0]), 'w')
		for out2 in output_conserved_2: f2.write('\n' + str(out2))
		f2.close()
		### Writing output3: Alignment in Fasta format
		f3 = open(r'%s_2_short.fasta' % (filename[0]), 'w')
		for out3 in output_conserved_3: f3.write('\n' + str(out3))
		f3.close()
		### Writing output4: Alignment in NESXUS format + Conserved block profile
		f4 = open(r'%s_2.nex' % (filename[0]), 'w')
		for out4 in output_conserved_4: f4.write('\n' + str(out4))
		f4.close()
		### Writing output4: Alignment in NESXUS format + Conserved block profile
		f5 = open(r'%s_2_short.nex' % (filename[0]), 'w')
		for out5 in output_conserved_5: f5.write('\n' + str(out5))
		f5.close()

#########################################################################
######                                                             ######
######          S E Q U E N C E   V E R I F I C A T I O N          ######
######                                                             ######
#########################################################################

########################
# RUN BEFORE ANALYZING #
########################
#This function check whether each input sequence is in FASTA format
def checkSeqFormat(inputText):
    if '>' not in inputText:
        return {'Fatal':True, 'error_messages':['The sequence is not in FASTA format']}
    splitInput = inputText.split('>')
    if splitInput[0]!='':
        return {'Fatal':True, 'error_messages':['The sequence is not in FASTA format']}
    del splitInput[0]
    #print(splitInput)
    for oneInput in splitInput:
        if oneInput!=oneInput.strip(' '):
            return {'Fatal':True, 'error_messages':['The sequence is not in FASTA format']}
    return True
    
	#This function check whether the input has been prepared by seqFIREprep
def checkPrepped(inputText):
	if '==seq==' not in inputText:
		return {'Fatal':True, 'error_messages':['The sequence is not properly prepped']}
	splitInput = inputText.split('==seq==')
	if splitInput[0]!='':
		return {'Fatal':True, 'error_messages':['The sequence is not properly prepped']}
	del splitInput[0]
	for oneInput in splitInput:
		if checkSeqFormat(oneInput)!=True:
			return {'Fatal':True, 'error_messages':['One of the sequence is not in FASTA format']}
	return True

#######################
# RUN AFTER ANALYZING #
#######################
''' 
Input for these functions is "seqList"
[[<Sequence name 1>,<Sequence 1>], [<Sequence name 2>,<Sequence 2>], ...]
'''
#This function check whether each input sequence is DNA or amino acid sequence
'''
Input: seqList and user selected sequence (selectedType)
Output: True if no error occurred, error list otherwise 

A sequence is not both DNA and amino acid sequence when
	1. The sequence consists of "J", "O", "U", "Z"
A sequence predicted as either DNA or amino acid sequence otherwise

Some letter in the sequence is extracted into 2 groups
	1. notDNA group: "E", "F", "I", "L", "P", "Q", "X"
	2. notProtein group: "B"

The sequence is then classified with this criteria:
	1. If the sequence consists of both notDNA and notProtein group -> Cannot determine
	2. If the sequence NOT consists of both notDNA and notProtein group
		If at least 90% of the sequence is "A", "T", "C", "G" -> DNA
		Otherwise -> Protein
	3. If the sequence only consists of notDNA group -> Protein
	4. If the sequence only consists of notProtein group -> DNA

The predicted sequence type (Verdict) is checked with user's selected sequence type
	Error will be raised when the verdict and selected sequence type does not match
'''
def checkSeqType(seqList,selectedType):
    verdict = ""
    errormsg = []
    for oneSeq in seqList:
        letter_dict = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0,'K': 0, 'L': 0, 'M': 0, 'N': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, '-': 0, '?': 0}
        #Exclude J, O, U, Z
        for oneLetter in oneSeq[1]:
            try:
                letter_dict[oneLetter] = letter_dict[oneLetter] + 1
            except:
                errormsg.append("FATAL ERROR: Detected invalid character in sequence %s" % (oneSeq[0]))
                break

        #Making prediction whether the sequence is DNA or RNA
        notDNAScore = letter_dict['E']+letter_dict['F']+letter_dict['I']+letter_dict['L']+letter_dict['P']+letter_dict['Q']+letter_dict['X']
        notProteinScore = letter_dict['B']
        if notDNAScore==0 and notProteinScore==0:
            DNAScore = letter_dict['A']+letter_dict['T']+letter_dict['C']+letter_dict['G']
            if DNAScore>=0.9*(sum(letter_dict.values())-letter_dict['-']-letter_dict['?']):
                verdict='DNA'
            else:
                verdict='Protein'
        elif notDNAScore>0 and notProteinScore>0:
            errormsg.append("FATAL ERROR: Detected invalid character in sequence %s" % (oneSeq[0]))
            continue
        elif notDNAScore>0:
            verdict='Protein'
        elif notProteinScore>0:
            verdict='DNA'

        #Test verdict with selected sequence type
        if verdict=="DNA" and selectedType == "Protein":
            errormsg.append("The sequence %s is detected as DNA" % (oneSeq[0]))
        elif verdict=="Protein" and selectedType =="DNA":
            errormsg.append("The sequence %s is detected as amino acid" % (oneSeq[0]))
    return errormsg if errormsg else True

#This function check if the input sequences are multiple aligned
'''
Input: seqList
Output: True if seqList is MSA, False otherwise

A sequence is MSA when the length of seqList is more than or equal to 2
All sequences must have the same length, or it will not be a valid MSA
'''
def checkMultipleSeq(seqList):
    if len(seqList)>=2:
        seqLength = len(seqList[0][1])
        for oneSeq in seqList:
            if len(oneSeq[1])!=seqLength:
                return ["FATAL ERROR: Inequal sequence length detected"]
        return True
    else:
        return ["FATAL ERROR: Single alignment detected"]

#This function check the alignment quality
'''
Input: seqList
Output: True if the quality of MSA is valid, error list otherwise

Validity of a sequence is evaluated from 2 criteria: Row validity and Column validity
    1. Row validity - A sequence with at least 40% CONTINUOUS GAP at head or tail will be considered invalid
'''
def checkMSAQuality(seqList):
    errormsg = []
    for oneSeq in seqList:
        headGap = 0
        tailGap = 0
        if oneSeq[1][0]=='-':
            for oneLetter in oneSeq[1]:
                if oneLetter=='-':
                    headGap = headGap+1
                else: break
        if oneSeq[1][-1]=='-':
            for oneLetter in oneSeq[1][::-1]:
                if oneLetter=='-':
                    tailGap = tailGap+1
                else: break
        biggestGap = headGap if headGap>tailGap else tailGap
        if biggestGap>=0.4*len(oneSeq[1]):
            errormsg.append('The sequence %s has at least 40% continuous gap at head or tail' % oneSeq[0])
    return errormsg if errormsg else True
    
#This function combines all 4 checking functions into one
'''
Input: seqList
Output: True if sequences are ready to analyze
'''
def checkReadiness(seqList, selectedType):
    errors = []
    errorDict = {'Fatal':False,'error_messages':[]}

    seqTypeResult = checkSeqType(seqList, selectedType)
    multipleSeqResult = checkMultipleSeq(seqList)
    MSAQualityResult = checkMSAQuality(seqList)
    
    if seqTypeResult!=True: errors.extend(seqTypeResult)
    if multipleSeqResult!=True: errors.extend(multipleSeqResult)
    if MSAQualityResult!=True: errors.extend(MSAQualityResult)

    for oneError in errors:
        if oneError.startswith('FATAL ERROR: '):
            errorDict['Fatal']=True
        errorDict['error_messages'].append(oneError)

    if errorDict['error_messages']!=[]:
        return errorDict
    else:
        return True

#########################################################################
######                                                             ######
######         S e q F I R E ' s   M A I N   P R O G R A M         ######
######                                                             ######
#########################################################################

if sys.argv[1:]==[]:
	usage()
	sys.exit(2)

try:                                
	opts, args = getopt.getopt(sys.argv[1:], "h:i:a:c:d:j:g:k:b:t:p:s:f:r:e:m:o:")

except (getopt.GetoptError):
	print("Invalid arguments")
	#usage()                          
	sys.exit(2)


for opt, arg in opts:                
	if opt == "-h":
		usage()
		sys.exit()
	if opt == "-i": infile = arg
	if opt == "-a": analysis_mode = int(arg)
	if opt == "-c": similarity_threshold = float(arg)
	if opt == "-d": percent_similarity = float(arg)
	if opt == "-j": percent_accept_gap = float(arg)
	if opt == "-g": p_matrix = arg
	if opt == "-k": p_matrix_2 = arg
	if opt == "-b": inter_indels = int(arg)
	if opt == "-t": twilight = str(arg)
	if opt == "-p": partial = str(arg)
	if opt == "-s": blocks = int(arg)
	if opt == "-f": fuse = int(arg)
	if opt == "-r": strick_combination = str(arg)
	if opt == "-e": combine_with_indel = str(arg)
	if opt == "-m": multidata = int(arg)
	if opt == "-o": output_mode = int(arg)

###################################
##   A N A L Y S I S   Z O N E   ##
###################################

if multidata == 1:
    f = open(r'%s' % (infile), 'r')
    record = f.read()
    f.close()
    if checkSeqFormat(record):
	    handle = parseFasta(record)
    else:
        raise Exception("FATAL ERROR: The input is not in FASTA format")
    readinessResult = checkReadiness(handle,'Protein')
    if readinessResult[0]!=True:
        if readinessResult[0]=='Fatal error':
            raise Exception(readinessResult[1])
        else:
            warnings.warn(readinessResult[1])
    if analysis_mode == 1: indelExtraction(handle) ### INDEL REGION MODULE ###
    elif analysis_mode == 2: conservedBlockExtraction(handle) ### CONSERVED BLOCK MODULE ###

elif multidata == 2:
	f = open(r'%s' % (infile), 'r')
	records = f.read().split('==seq==')
	f.close()
	del records[0]
	for record in records:
		a = record.split('==fire==')
		filename = a[0]
		print (filename)
		handle = parseFasta(a[1])
		if checkReadiness(handle)==False: warnings.warn("Something is wrong!")

		if output_mode == 1 or output_mode == 3:
			print ('==seq==%s==fire==' % filename)
		elif output_mode == 2 or output_mode == 3:
			f = open(r'outfile.txt', 'a')
			f.write('\n==seq==%s==fire==\n' % filename)
			f.close()

		if analysis_mode == 1: indelExtraction(handle) ### INDEL REGION MODULE ###
		elif analysis_mode == 2: conservedBlockExtraction(handle) ### CONSERVED BLOCK MODULE ###
