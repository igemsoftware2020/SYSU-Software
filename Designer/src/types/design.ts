export interface Design {
  /** 该通路图的唯⼀标识 */
  persistentIdentity: string;
  article: string | null;
  description: string | null;
  // 表⽰⼀个活动（⽐如，通路图的创建活动等）。
  Activity: [];
  ComponentDefinition: ComponentDefinition[];
}

export interface Sequence {
  persistentIdentity: string;
  displayId: string;
  version: string;
  wasDerivedFrom: string;
  wasGeneratedBy: string;
  topLevel: string;
  ownedBy: string[];
  elements: string;
  encoding: string;
  father_id: string;
}

export interface Location {
  persistentIdentity: string;
  displayId: string;
  version: string;
  topLevel: string;
  direction: string;
  start: number;
  end: number;
  orientation: string;
  father_id: string;
}

export interface Component {
  persistentIdentity: string;
  displayId: string;
  version: string;
  title: string;
  topLevel: string;
  definition: string;
  access: string;
  father_id: string;
}

export interface SequenceAnnotation {
  persistentIdentity: string;
  displayId: string;
  version: string;
  title: string;
  topLevel: string;
  component: string;
  father_id: string;
  Location: Location[];
}

export interface ComponentDefinition {
  persistentIdentity: string;
  displayId: string;
  version: string;
  wasDerivedFrom: string;
  wasGeneratedBy: string;
  title: string;
  description: string;
  created: string;
  modified: string;
  mutableProvenance: string;
  topLevel: string;
  mutableDescription: string;
  mutableNotes: string;
  creator: string;
  type: string;
  role: string;
  Sequence: Sequence[];
  Component: Component[];
  SequenceAnnotation: SequenceAnnotation[];
}

export const PartTypes: Record<string, { image: any; name: string }> = {
  aptamer: {
    name: "Aptamer",
    image: require("url:../assets/part_icons/aptamer.png"),
  },
  binding_site: {
    name: "Binding Site",
    image: require("url:../assets/part_icons/binding_site.png"),
  },
  cds: { name: "CDS", image: require("url:../assets/part_icons/cds.png") },
  cell: { name: "Cell", image: require("url:../assets/part_icons/cell.png") },
  composite: {
    name: "Composite",
    image: require("url:../assets/part_icons/composite.png"),
  },
  device: {
    name: "Device",
    image: require("url:../assets/part_icons/device.png"),
  },
  dna: { name: "DNA", image: require("url:../assets/part_icons/dna.png") },
  gene: { name: "Gene", image: require("url:../assets/part_icons/gene.png") },
  generator: {
    name: "Generator",
    image: require("url:../assets/part_icons/generator.png"),
  },
  interval: {
    name: "Interval",
    image: require("url:../assets/part_icons/interval.png"),
  },
  origin_of_replication: {
    name: "Origin of Replication",
    image: require("url:../assets/part_icons/origin_of_replication.png"),
  },
  plasmid: {
    name: "Plasmid",
    image: require("url:../assets/part_icons/plasmid.png"),
  },
  primer: {
    name: "Primer",
    image: require("url:../assets/part_icons/primer.png"),
  },
  primer_binding_site: {
    name: "Primer Binding Site",
    image: require("url:../assets/part_icons/primer_binding_site.png"),
  },
  promoter: {
    name: "Promoter",
    image: require("url:../assets/part_icons/promoter.png"),
  },
  protein: {
    name: "Protein",
    image: require("url:../assets/part_icons/protein.png"),
  },
  protein_stability_element: {
    name: "Protein Stability Element",
    image: require("url:../assets/part_icons/protein_stability_element.png"),
  },
  rbs: { name: "RBS", image: require("url:../assets/part_icons/rbs.png") },
  reporter: {
    name: "Reporter",
    image: require("url:../assets/part_icons/reporter.png"),
  },
  ribonuclease_site: {
    name: "Ribonuclease Site",
    image: require("url:../assets/part_icons/ribonuclease_site.png"),
  },
  rna: { name: "RNA", image: require("url:../assets/part_icons/rna.png") },
  rna_stability_element: {
    name: "Rna Stability Element",
    image: require("url:../assets/part_icons/rna_stability_element.png"),
  },
  scar: { name: "Scar", image: require("url:../assets/part_icons/scar.png") },
  terminator: {
    name: "Terminator",
    image: require("url:../assets/part_icons/terminator.png"),
  },
  tf: { name: "TF", image: require("url:../assets/part_icons/tf.png") },
  transcription_end_site: {
    name: "Transcription End Site",
    image: require("url:../assets/part_icons/transcription_end_site.png"),
  },
  translation: {
    name: "Translation",
    image: require("url:../assets/part_icons/translation.png"),
  },
  translation_end_site: {
    name: "Translation End Site",
    image: require("url:../assets/part_icons/translation_end_site.png"),
  },
  unknown: {
    name: "Unknown",
    image: require("url:../assets/part_icons/unknown.png"),
  },
};

export type IPartType =
  | "aptamer"
  | "binding_site"
  | "cds"
  | "cell"
  | "composite"
  | "device"
  | "dna"
  | "gene"
  | "generator"
  | "interval"
  | "origin_of"
  | "parts"
  | "parts_db"
  | "plasmid"
  | "primer"
  | "primer_binding"
  | "promoter"
  | "protein"
  | "protein_stability"
  | "rbs"
  | "reporter"
  | "ribonuclease_site"
  | "rna"
  | "rna_stability"
  | "scar"
  | "terminator"
  | "tf"
  | "transcription_end"
  | "translation"
  | "translation_end"
  | "unknown";

export const SequenceEncodings = [
  {
    name: "IUPAC DNA, RNA",
    uri: "http://www.chem.qmul.ac.uk/iubmb/misc/naseq.html",
  },
  {
    name: "IUPAC Protein",
    uri: "http://www.chem.qmul.ac.uk/iupac/AminoAcid/",
  },
  {
    name: "SMILES",
    uri: "http://www.opensmiles.org/opensmiles.html",
  },
];

export const roleArrayToType = (roles: string[]): IPartType => {
  return (roles[0] ?? "unknown") as IPartType;
};
