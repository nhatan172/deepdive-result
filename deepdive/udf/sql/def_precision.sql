SELECT dm.mention_id
    , dm.concept_expression
    , dm.explain_text
    , dfi.expectation

  FROM has_definition_inference  dfi,
	 definition_mention dm

 WHERE  expectation >= 0.6
	AND dfi.mention_id = dm.mention_id
 ORDER BY random()
 LIMIT 100
