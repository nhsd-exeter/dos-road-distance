# ADR-004: Road Distance Provider

* Date: 2021/03/22
* Status: Proposed
* Deciders: Jay Bush, Nick Miles, Jayne Chapman, Dan Stefaniuk, Tamara Goldschmidt

## Context

DoS currently calculates and presents a straight-line distance between the patient's postcode and each of the returned services. Often this is sufficiently accurate, but for more rural areas or certain service types of which there are fewer available services and therefore the distances are longer, or for areas close to a body of water, distances can be very inaccurate and cause sub-optimal results to return.

To solve this issue we would like to calculate a road distance between the patient and each service, and return those which are closer. DoS does not currently contain the data or functionality to determine accurate point to point road distances between patients and services. In the interests of development speed a third party API will be used to obtain the required distances.

Requirements:

- Replace services in search where road distance is closer than DoS distance (i.e. returned services are more reasonable for patient to travel to).
- Patient's mode of transport will not be known or asked for therefore the calculation will be based on fastest route by car.
- Timeframes and modes of transport are variable and therefore speed of travel is not taken into account (e.g. disposition time of 12 hours means travel time cannot be accurately determined)
- Call handlers do not require and will not be expected to acquire patient mode of transport, routes or live traffic information.
- The CCS search average response time remains within the current SLA (3.2 seconds).

## Decision

A number of providers were examined while researching options for road distancing:

| Provider    | Method of selecting route                                                                                                  | Notes                                                                                                                                                                                                 | Monthly Est. Cost  |
| ----------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| Bing        | Distance of the route with the shortest average travel time by car. Possible option for shortest distance (different api). | A standard distance matrix can have up to 625 origin-destination pairs. Quoted for varying prices depending upon usage - estimates indicate that we would require the Usage c30M Transactions bundle. | £11,538.00         |
| Geoapify    | Shortest distance by car                                                                                                   | Limited to 2.5m requests per month and 20 requests per second. Very small organisation. Distance API is in beta.                                                                                      | 1000 euro          |
| Travel Time | Distance of the route with the shortest average travel time by car.                                                        | No cap on number of locations requested per call or number of requests. Very responsive to requests for information or help.                                                                          | £5,200 (flat rate) |
| Google      | Distance of the route with the shortest average travel time by car. Option for shortest distance by car.                   | Google has not been contacted as the number of elements per request (25) we require would exceed their advertised limits.                                                                             |                    |

Advertised costs for Bing and Google are roughly in line with each other, while Travel Time and Geoapify are significantly cheaper. We have an account with Bing that could quickly be increased to include our required usage. We have an account with Google (but I believe this has been procured differently, as finance do not seem to be aware of it). We have not yet approached Google for costs to include our usage. NHS Digital has an existing relationship with Travel Time (contact tracing). Geoapify would require new procurement.

Google and Geoapify were found to be unable to scale to the level of calls required by the DoS search, or imposed unacceptable limits on the number of services that could be profiled in the single call. While possible to make multiple calls for a single DoS search, the additional overhead was deemed unacceptable.

Bing and Travel Time are both able to produce similar distance data, meeting the level of calls DoS requires, and NHS Digital has existing relationships with both organisations. However, Bing is significantly more expensive with a potential for sudden price increases if usage exceeds a current pricing tier. Bing's request cap of 625 origin / destination pairs also poses some issues considering around 10% of DoS queries would potentially need to query more than this number of eligible services.

The suggested provider is Travel Time, on the basis of lower costs and having stood apart in terms of engagement with our proposals, and how quickly they have been able to respond to queries.

## Consequences

- Due to the number of services returned in a search it may not be possible to obtain road distances for all eligible services. Following sorting by crow flies, distances for the top N services will be obtained. The number of services N will be defined by experimentation. It is very difficult to ascertain which services might be affected and there is risk any such implementation may not be useful in 100% of searches.
- Most third party distance matrix APIs return the fastest route as opposed to the shortest route. This means that, over time, services may appear in a different order or not be returned.
- The logic used to determine the route is not always evident or well documented, and it may not be possible to fully understand why a given route is returned. Fundamentally, any background logic in the selection of a route for a distance matrix would be subject to change, possibly without notice.

### Traffic and other factors affecting search results

Additional consideration if traffic or other variables are factored into the search

- Adding any mitigation for traffic or other factors that could change the route retuned over short timescales makes profiling of services much more difficult and search returns less predictable.
- Realtime or near realtime identification of delays would not be able to take into account the journey time to that point, or patient mode of travel and may result in appropriate services being excluded from the search.
- Additional factors in route selection decisions will increase processing overhead by an unknown amount, increasing response times.
- Many one hour disposition outcomes result in a patient callback. These would not benefit from traffic calculations. Team is currently discussing with Steven McIntyre what proportion of one hour dispositions would require physical road distances (i.e. the patient has to travel).

With any third-party API additional development work will be required to integrate with DoS, including to gracefully handle errors from, or unavailability of, the external API.
