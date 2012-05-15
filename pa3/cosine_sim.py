from util import *

#def cosine_sim(train_data, train_rel, test_data)
if __name__ == "__main__":
    weights = [0.50, 0.30, 0.20]
    dictionary = read_dictionary()
    queries = read_train_data()
    corpus = read_corpus()
    for q in queries:
        pq = l1_normalize(parse_query(q.query_terms, dictionary, corpus))
        scored_urls = []
        for url in q.query_results:            
            body_windwo = url.minimum_body_window(q.query_terms)
            anchor_vector = normalized_raw_term_scores(url.prepare_anchors(dictionary), dictionary)
            body_vector = sublinear_term_scores(url.prepare_body(dictionary), dictionary)
            title_vector = normalized_raw_term_scores(url.prepare_title(dictionary), dictionary)
            anchor_vector = l1_normalize(anchor_vector)
            body_vector = l1_normalize(body_vector)
            title_vector = l1_normalize(title_vector)
            anchor_vector = mul(weights[0], anchor_vector)
            body_vector = mul(weights[1], body_vector)
            title_vector = mul(weights[2], title_vector)
            weighted_vector = add(add(anchor_vector, body_vector), title_vector)
            score = dot(pq, weighted_vector)
            scored_urls.append((score, url.url))
        # output the urls in order
        print "query: " + q.query_terms
        scored_urls.sort(reverse=True)
        for (s,u) in scored_urls:
            print " url: " + u
    with open('Weights','w') as f:
        weights.reverse()
        f.write(" ".join(map(lambda n : str(n), weights)))
