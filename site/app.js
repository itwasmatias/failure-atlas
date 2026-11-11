"use strict";
(() => {
  const cases = globalThis.FAILURE_ATLAS_CASES;
  const $ = id => document.getElementById(id);
  const stop = new Set("the a an is and or to in of for at after before from with without into on of that this were are was have has across many much how new more would what when than had about service services".split(" "));
  const labels = {
    "cf-2019-07-02":"Cloudflare · July 2019",
    "github-2018-10-21":"GitHub · October 2018",
    "cf-2020-07-17":"Cloudflare · July 2020"
  };
  const headline = {
    "cf-2019-07-02":"An unexpected web firewall outage",
    "github-2018-10-21":"A database incident after network separation",
    "cf-2020-07-17":"A routing change concentrates traffic"
  };
  function node(tag, className, text) {
    const item = document.createElement(tag);
    if (className) item.className = className;
    if (text !== undefined) item.textContent = text;
    return item;
  }
  function paragraph(label, content) {
    const result = node("p");
    const strong = node("strong",null,label+" ");
    result.append(strong,document.createTextNode(content));
    return result;
  }
  function sourceLink(item) {
    const link = node("a","source-link","Read original incident report ↗");
    link.href = item.url;
    link.target="_blank";
    link.rel="noopener noreferrer";
    return link;
  }
  function terms(text) {
    const words=(text.toLowerCase().match(/[a-z0-9]+/g)||[])
      .filter(term => term.length >= 3 && !stop.has(term));
    return new Set(words);
  }
  function rank(query) {
    const q = terms(query);
    return cases.map(item => {
      const incident = terms(item.symptoms);
      const common = [...q].filter(word => incident.has(word));
      return {item, common};
    }).filter(match => match.common.length > 0)
      .sort((a,b)=>b.common.length-a.common.length || a.item.case_id.localeCompare(b.item.case_id));
  }
  function card(item) {
    const article = node("article","case-card");
    article.append(node("span","case-id",item.case_id.toUpperCase()));
    article.append(node("h3",null,headline[item.case_id] || item.case_id));
    article.append(paragraph("Observed symptoms:",item.symptoms));
    article.append(paragraph("Documented explanation:",item.cause));
    article.append(paragraph("Reported response:",item.resolution));
    const source=node("div","source");
    source.append(sourceLink(item));
    article.append(source);
    return article;
  }
  function show(query) {
    const matches=rank(query);
    const target=$("match-results");
    target.replaceChildren();
    if (!matches.length) {
      target.append(node("div","empty","No symptom keywords overlap the three archived cases. This is not evidence that your issue has no precedent — expand the corpus and investigate your own logs."));
      return;
    }
    for (const {item,common} of matches) {
      const entry=node("article","match");
      entry.append(node("span","match-title",labels[item.case_id] || item.case_id));
      entry.append(node("h3",null,headline[item.case_id] || item.case_id));
      entry.append(node("div","matched","Matching terms: "+common.join(", ")));
      entry.append(paragraph("What engineers reported:",item.symptoms));
      entry.append(paragraph("What the postmortem attributed it to:",item.cause));
      entry.append(paragraph("Documented response:",item.resolution));
      entry.append(node("div","why","Use this case as a lead for investigation, not proof of the same cause. Check independent signals in your own service before taking action."));
      entry.append(sourceLink(item));
      target.append(entry);
    }
  }
  if (!Array.isArray(cases) || cases.length !== 3) {
    $("match-results").replaceChildren(node("div","empty","Public incident data unavailable."));
    return;
  }
  const grid=$("case-grid");
  for (const item of cases) grid.append(card(item));
  $("search-form").addEventListener("submit", event => {
    event.preventDefault();
    show($("query").value);
  });
  document.querySelectorAll("[data-query]").forEach(button => {
    button.addEventListener("click", () => {
      $("query").value=button.dataset.query;
      show(button.dataset.query);
    });
  });
})();
