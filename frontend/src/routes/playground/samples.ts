export const samples: Record<string, { spec: string; data: string }> = {
	'image-classification': {
		spec: JSON.stringify(
			{
				data: { type: 'image' },
				label: { type: 'text' },
				output: { type: 'text' }
			},
			null,
			2
		),
		data: JSON.stringify(
			{
				data: 'https://pandas.pydata.org/docs/_static/pandas.svg',
				label: 'zeno',
				output: 'zeno'
			},
			null,
			2
		)
	},
	'text-classification': {
		spec: JSON.stringify(
			{
				data: { type: 'text' },
				label: { type: 'text' },
				output: { type: 'text' }
			},
			null,
			2
		),
		data: JSON.stringify(
			{
				data: 'test',
				label: 'zeno',
				output: 'zeno'
			},
			null,
			2
		)
	},
	'space-separated-values': {
		spec: JSON.stringify(
			{
				data: { type: 'separatedValues', header: 'Data', separator: ' ' },
				label: {
					type: 'separatedValues',
					header: 'Label',
					highlight: true,
					separator: ' '
				},
				output: {
					type: 'separatedValues',
					header: 'Output',
					separator: ' '
				},
				displayType: 'table'
			},
			null,
			2
		),
		data: JSON.stringify(
			{
				data: 'test a b c\ntest a b c',
				label: 'testfsdfs aasd b c\ntest a b c',
				output: 'test a b c\ntest aasdfd b c'
			},
			null,
			2
		)
	},
	'audio-transcription': {
		spec: JSON.stringify(
			{
				data: { type: 'audio' },
				label: { type: 'text' },
				output: { type: 'text' }
			},
			null,
			2
		),
		data: JSON.stringify(
			{
				data: 'https://github.com/apple/ml-symphony/raw/main/symphony_lib/static/symphony-audio-sample.mp3',
				label: 'zeno',
				output: 'zeno'
			},
			null,
			2
		)
	},
	chatbot: {
		spec: JSON.stringify(
			{
				data: {
					type: 'list',
					elements: {
						type: 'message',
						content: {
							type: 'text'
						}
					},
					collapsible: 'top'
				},
				label: {
					type: 'message',
					plain: true,
					role: 'assistant',
					highlight: false,
					content: {
						type: 'text'
					}
				},
				output: {
					type: 'message',
					plain: true,
					role: 'assistant',
					highlight: true,
					content: {
						type: 'text'
					}
				}
			},
			null,
			2
		),
		data: JSON.stringify(
			{
				data: [
					{
						role: 'assistant',
						content: 'Hello this is Jane at Rivertown Insurance. How can I help you today?'
					},
					{
						role: 'user',
						content: 'Hi, this is Joe Last and I would like to pay my auto insurance bill.'
					},
					{
						role: 'assistant',
						content: 'Hello again, this is Jane at Rivertown Insurance. How can I help you today?'
					},
					{
						role: 'user',
						content: 'Hi, again, this is Joe Last and I would like to pay my auto insurance bill.'
					},
					{
						role: 'assistant',
						content: 'Hello finally, this is Jane at Rivertown Insurance. How can I help you today?'
					},
					{
						role: 'user',
						content: 'Hi, finally this is Joe Last and I would like to pay my auto insurance bill.'
					}
				],
				label:
					'Okay mister Last. I can help you with payment. #Ah first I will need your account number please.',
				output:
					'Hello Joe, thank you for choosing Rivertown Insurance as your insurance provider. I can definitely assist you with that. Do you have your policy number and payment information handy?'
			},
			null,
			2
		)
	},
	'chatbot-markdown': {
		spec: JSON.stringify(
			{
				data: {
					type: 'list',
					elements: {
						type: 'message',
						content: {
							type: 'markdown'
						}
					},
					collapsible: 'top'
				},
				label: {
					type: 'message',
					plain: true,
					role: 'assistant',
					highlight: false,
					content: {
						type: 'markdown'
					}
				},
				output: {
					type: 'message',
					plain: true,
					role: 'assistant',
					highlight: true,
					content: {
						type: 'markdown'
					}
				}
			},
			null,
			2
		),
		data: JSON.stringify(
			{
				data: [
					{
						role: 'assistant',
						content: 'Hello **this** is Jane at Rivertown Insurance. How can I help you today?'
					},
					{
						role: 'user',
						content: 'Hi, this is Joe Last and I would like to pay my auto insurance bill.'
					}
				],
				label:
					'Okay ~mister~ Last. I can help you with payment. #Ah first I will need your account number please.',
				output:
					'# test \n Hello Joe, thank you for choosing Rivertown Insurance as your insurance provider. I can definitely assist you with that. Do you have your policy number and payment information handy?'
			},
			null,
			2
		)
	},
	'code-generation': {
		spec: JSON.stringify(
			{
				data: { type: 'code' },
				label: { type: 'code' },
				output: { type: 'code' }
			},
			null,
			2
		),
		data: JSON.stringify(
			{
				data: '# sort list of strings',
				label: 'sorted_list = sorted(my_list)',
				output:
					"my_list = ['apple', 'banana', 'cherry']\nsorted_list = sorted(my_list)\nprint(sorted_list)"
			},
			null,
			2
		)
	},
	rag: {
		spec: JSON.stringify(
			{
				data: { type: 'text' },
				label: { type: 'text' },
				output: {
					type: 'vstack',
					keys: {
						answer: { type: 'text' },
						retrieved: {
							type: 'list',
							elements: {
								type: 'vstack',
								keys: {
									score: { type: 'text', label: 'score: ' },
									reference: { type: 'text', label: 'id: ' },
									text: { type: 'text', label: 'text: ' }
								}
							},
							collapsible: 'bottom',
							border: true,
							pad: true
						}
					}
				}
			},
			null,
			2
		),
		data: JSON.stringify(
			{
				data: 'what do the 3 dots mean in math',
				output: {
					answer: 'they are magic dots',
					retrieved: [
						{
							reference: '11259078_10',
							text: 'BULLET::::3. Karen Salmansohn as Huffington Post columnist (What Do You Tell Kids When They Ask Why Mean People Are Mean? (And what do you tell yourself too?))',
							score: 11.97700023651123
						},
						{
							reference: '43266366_5',
							text: '3. "What Do We Mean To Each Other"',
							score: 11.40779972076416
						},
						{
							reference: '15587152_6',
							text: 'BULLET::::2. "Do You Know What I Mean" \u2013 3:45',
							score: 10.996999740600586
						},
						{
							reference: '28286148_8',
							text: 'BULLET::::- Side A "Do You Know What I Mean" - 3:20',
							score: 10.99699878692627
						},
						{
							reference: '50920027_10',
							text: 'BULLET::::6. "Do You Know What I Mean" - 3:11',
							score: 10.996997833251953
						},
						{
							reference: '54315209_7',
							text: 'BULLET::::3. "Do You Know What It Means to Miss New Orleans?" (Louis Alter, Eddie DeLange) \u2013 3:30',
							score: 10.90369987487793
						},
						{
							reference: '7196002_23',
							text: 'BULLET::::3. "What Do We Mean to Each Other" (duet with Kevyn Lettau)',
							score: 10.866600036621094
						},
						{
							reference: '7382309_50',
							text: 'BULLET::::15. "Do You Know What I Mean" \u2013 Lee Michaels \u2013 3:14',
							score: 10.7391996383667
						}
					]
				}
			},
			null,
			2
		)
	}
};
