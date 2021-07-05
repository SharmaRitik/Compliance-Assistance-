      def GDPR ( Engine , Input_question):
        engine = sqlalchemy.create_engine('mysql+pymysql://root:@127.0.0.1:3306/qusetionanswer')
        query = '''
        select a.DocumentName,b.HeadingName,b.HeadingContext,LOWER(c.QuestionText) QuestionText ,c.AnswerText 
        from documentmaster a join documentheadings b on a.DocumentID=b.DocumentID join documentqa c on b.DocumentHeadingID=c.HeadingID
        '''
        df = pd.read_sql_query(query, engine)

        ques_list = list(ques for ques in df['QuestionText'])
        ans_list = list(ans for ans in df['AnswerText'])  ## Qu = Input german question
        laser = Laser()
        Input_Emb = laser.embed_sentences([Qu],lang=['de'])[0] 
        sim_result = []
        for question in ques_list:
            sentence_embeddings = laser.embed_sentences([question],lang=['de'])[0]
            sim_result.append(cosine_similarity(sentence_embeddings.reshape(1, -1), Input_Emb.reshape(1, -1)))

        an = np.argmax(sim_result)
        if sim_result[an] > 0.9:
            print(str(sim_result[an]))
            return ans_list[an]

        else:
            return -1
