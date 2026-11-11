# ![Unillustrated prototype](placeholder.svg) Undissection: Lift a glass

A hand lifts a glass. What does the rest of the body contribute? Put the parts together and find out.

> NOTE: Gameplay-only explanatory model for grades 8–10. Existing plain placeholder, no anatomical artwork. Early mechanical demonstrations show what arrangements permit; they do not claim isolated parts can live without support. The active brief owns included supporting anatomy and the school-level boundary.

## `arm-chapter` A muscle can only pull
background: ![Plain work surface](placeholder.svg)

Start with an arm in a body model. Before giving it supplies or instructions, arrange its parts so that it can bend and straighten.

**Goals**

- Make an arm with a movable elbow -- Arm
- next: Give the arm a pull in each direction -- Arm[Bending muscles,Straightening muscles]

**Items**

- Arm bones

  The bones of the upper arm, forearm and hand. The wrist, hand and shoulder's supporting structures are included; the elbow is the joint being reconstructed here.

- Elbow joint

  The place where the arm bones meet and can turn relative to one another. It includes the tissues that hold the bones together and allow smooth movement.

- Bending muscles

  Muscles with their tendons: strong bands attaching muscle to bone. This group pulls across the front of the elbow to bend the arm. Other ordinary supporting muscles are included in the model.

- Straightening muscles

  Muscles with their tendons attached on the other side of the elbow. Their pull can straighten the arm.

- Arm (compound)
  - slot: Pull to bend, accepts Bending muscles
  - slot: Pull to straighten, accepts Straightening muscles

  The joint lets the forearm turn. Bones provide rigid support that can turn at a joint, but they do not pull themselves into a new position.

- Arm

  [Bending muscles]

  When this muscle group shortens, tendons—the bands attaching muscle to bone—pull the forearm into a bend. Relaxing the muscle eases its pull; it cannot push the bones back the other way.

- Arm

  [Straightening muscles]

  This group pulls through tendons, the bands attaching muscle to bone, from the other side of the joint. That straightens the elbow. A different direction of movement still comes from a pull.

- Arm

  [Bending muscles,Straightening muscles]

  The arm now has opposing pulls. The muscles can work together to bend, straighten and hold the joint steady. This arrangement gives the body a way to position the hand.

  ---

  Muscles can also control movement while lengthening. For example, slowly lowering a held weight can involve the bending muscles braking the motion. Opposing pulls are a useful starting model, not a rule that only one muscle works at a time.

  Reference: [OpenStax, Muscle interactions](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-1-interactions-of-skeletal-muscles-their-fascicle-arrangement-and-their-lever-systems).

**Combinations**

- Elbow joint [consume] + Arm bones [consume] -> Arm (tutorial)

## `control-chapter` Where should the hand go?
background: ![Plain work surface](placeholder.svg)

The arm's parts allow movement, but a useful reach needs direction. Connect what the body sees to the muscles that position its hand.

**Goals**

- Connect sight to a route for messages -- Seeing nervous system
- next: Give the arm a connection to that control -- Guided arm

**Items**

- Brain and spinal cord

  The brain interprets information and helps plan movement. The spinal cord links much of the body to the brain and also takes part in control.

- Nerves

  Connections that carry signals between the body's sense organs, central control and muscles. Signals are messages, not supplies of food or oxygen.

- Eyes

  Sense organs that detect light. Their signals give the brain information about objects and their positions.

- Connected nervous system

  Nerves give messages a route between the brain, spinal cord and body. Some signals bring information in; others tell muscles to pull. This lets the brain coordinate different muscles.

- Seeing nervous system

  The eyes detect light and send signals. The brain can use that information to work out where an object is. Seeing supplies information about where to reach; it does not provide the force to move an arm.

- Guided arm

  The nerve connections let the brain coordinate the arm's muscle pulls. Signals from the body also report its position. The model now links information to movement—but those muscles still need continuing supplies to do their work.

**Combinations**

- Nerves [consume] + Brain and spinal cord [consume] -> Connected nervous system
- Eyes [consume] + Connected nervous system [transform] -> Seeing nervous system
- Seeing nervous system [consume] + Arm[Bending muscles,Straightening muscles] [transform] -> Guided arm

## `air-chapter` Oxygen has to reach the arm
background: ![Plain work surface](placeholder.svg)

Air goes into the lungs, far from the muscles in the arm. Build the route that carries oxygen from one to the other.

**Goals**

- Make a returning blood circuit and a way to move air
  - both: Circulation
  - and: Breathing lungs
- next: Connect breathing to blood flow -- Heart and lungs

**Items**

- Heart

  A muscular pump with chambers and valves that keep blood moving in the intended direction. The heart generates its own rhythm; nerves can adjust its activity.

- Blood-filled vessels

  Arteries carry blood away from the heart; veins return it. Tiny connecting vessels run close to body cells, where substances pass between blood and the surrounding tissues. Lung and body routes are included.

- Lungs

  Organs with many small air spaces beside tiny blood vessels. Their thin surfaces allow gases to pass between air and blood.

- Breathing muscles

  Muscles that change the space inside the chest, including the diaphragm beneath the lungs. Their ordinary chest-wall support is included.

- Circulation

  The heart pushes blood through vessels and receives it back. This returning flow is circulation. It carries supplies toward cells—the tiny living units that make up muscles and other body parts—and takes substances away. A pump needs a connected route to make those deliveries.

- Breathing lungs

  Breathing muscles expand the chest: the diaphragm, a muscle beneath the lungs, pulls downward, while other muscles lift the ribs. The lungs expand and air flows in. When these muscles relax during quiet breathing, the chest and lungs spring back and air flows out. Moving air is a different job from moving blood.

- Heart and lungs

  Oxygen crosses from air through the thin walls into blood. The heart sends this blood onward to the body. Blood brings back carbon dioxide made by body cells; this gas crosses into the lungs and is breathed out. The blood route is heart → lungs → heart → body → heart.

  ---

  Body cells can use oxygen to release energy from nutrients, producing carbon dioxide. The lungs exchange gases; they do not create energy or pump blood. The circulatory loop includes heart → lungs → heart → body → heart.

  Reference: [OpenStax, Gas exchange](https://openstax.org/books/anatomy-and-physiology-2e/pages/22-4-gas-exchange).

**Combinations**

- Heart [consume] + Blood-filled vessels [consume] -> Circulation
- Breathing muscles [consume] + Lungs [consume] -> Breathing lungs
- Breathing lungs [consume] + Circulation [transform] -> Heart and lungs

## `whole-chapter` More than an arm
background: ![Plain work surface](placeholder.svg)

Oxygen alone does not supply a muscle with fuel. Connect food's route into the same blood supply, then bring the parts together for the reach.

**Goals**

- Connect a meal to the body's supply route -- Heart, lungs and gut
- next: Bring supply and control together in the body -- Body ready to reach
- next: Reach for the glass and lift it -- Body lifting a glass

**Items**

- Stomach

  A muscular part of the gut that mixes food with digestive juices and starts breaking down some of its contents. Ordinary preparation by the mouth is included in this short model.

- A meal

  Food provides nutrients: substances the body uses for energy, growth and repair. This represents supply over time, not an instant power-up for the next movement.

- Small intestine

  A long, folded part of the gut. Here digestion continues and nutrients cross its lining into the body's internal transport routes. Digestive juices from other glands and the lining's transport support are included.

- Glass of water

  A glass within reach on a table. The task is to see its position, reach accurately and lift it; drinking is outside this episode.

- Stomach working on a meal

  The stomach mixes and partly breaks down the meal. Its nutrients—substances used for energy, growth and repair—are not yet available to an arm muscle. They still need to cross from the gut into the body's transport system.

- Gut supplying nutrients

  Digestion continues in the small intestine. Nutrients cross its lining: simple sugars, for example, enter nearby blood vessels. Breaking food down is digestion; moving usable substances across the lining is absorption. The arm cannot use a piece of food still sitting in the stomach.

- Heart, lungs and gut

  The same circulation now brings oxygen from the lungs and nutrients from the gut. Cells use nutrients to release energy for work, often with oxygen. A muscle needs both a delivery route and things worth delivering. Absorbing a meal takes time; stored fuel lets us move between meals.

  ---

  Digestion and absorption take time. Muscles already have access to stored fuel, so a person can move before a new meal is absorbed. Different nutrients take different routes; many fats enter lymph vessels before joining the bloodstream. This model follows the shared supply relationship without reconstructing those details.

  Reference: [OpenStax, Digestion and absorption](https://openstax.org/books/anatomy-and-physiology-2e/pages/23-7-chemical-digestion-and-absorption-a-closer-look).

- Body ready to reach

  The arm's muscles now belong to the same model as its supplies and control. Blood delivers oxygen and nutrients; nerves carry signals. Those are different jobs. Muscles use energy to pull on bones. Information about what the eyes see and where the arm is helps the brain coordinate the movement.

- Body lifting a glass

  The hand reaches, grips and lifts. Now hold the glass still. The arm has stopped moving, but its muscles keep pulling against the glass's weight—and using energy. Nerve signals adjust those pulls; blood continues bringing supplies and carrying carbon dioxide away.

  One body remains. Even keeping a hand still involves work throughout it, supported by food and air from outside.

**Combinations**

- A meal [consume] + Stomach [transform] -> Stomach working on a meal
- Small intestine [consume] + Stomach working on a meal [transform] -> Gut supplying nutrients
- Gut supplying nutrients [consume] + Heart and lungs [transform] -> Heart, lungs and gut
- Heart, lungs and gut [consume] + Guided arm [transform] -> Body ready to reach
- Glass of water [consume] + Body ready to reach [transform] -> Body lifting a glass
