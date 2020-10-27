import * as React from "react";
import { MenuItem, HTMLTable, AnchorButton, NonIdealState, H2, Classes } from "@blueprintjs/core";
import { Suggest, ItemRenderer } from "@blueprintjs/select";
import { useElement } from "../hooks/api";
import { DraggablePart } from "./Part";
import {} from "react-dnd";
import { ComponentDefinition, PartTypes, roleArrayToType } from "../types/design";
import { useDebounce } from "use-debounce";
import { IconNames } from "@blueprintjs/icons";

function escapeRegExpChars(text: string) {
  return text.replace(/([.*+?^=!:${}()|\\[\]\\/\\])/g, "\\$1");
}

function highlightText(text: string, query: string) {
  let lastIndex = 0;
  const words = query
    .split(/\s+/)
    .filter((word) => word.length > 0)
    .map(escapeRegExpChars);
  if (words.length === 0) {
    return [text];
  }
  const regexp = new RegExp(words.join("|"), "gi");
  const tokens: React.ReactNode[] = [];
  for (;;) {
    const match = regexp.exec(text);
    if (!match) {
      break;
    }
    const length = match[0].length;
    const before = text.slice(lastIndex, regexp.lastIndex - length);
    if (before.length > 0) {
      tokens.push(before);
    }
    lastIndex = regexp.lastIndex;
    tokens.push(<strong key={lastIndex}>{match[0]}</strong>);
  }
  const rest = text.slice(lastIndex);
  if (rest.length > 0) {
    tokens.push(rest);
  }
  return tokens;
}

export const Search: React.FunctionComponent = () => {
  const [rawQuery, onRawQueryChange] = React.useState("");
  const [query] = useDebounce(rawQuery, 250);

  const { data: res, loading } = useElement(query);
  const data = React.useMemo(() => Object.values(res?.response ?? {}), [res]);

  const [selected, setSelected] = React.useState<ComponentDefinition | null>(null);

  const inputValueRenderer = React.useCallback((item: ComponentDefinition) => item.displayId, []);
  const itemRenderer: ItemRenderer<ComponentDefinition> = React.useCallback(
    (item: ComponentDefinition, { handleClick, modifiers, query }) => (
      <MenuItem
        label={PartTypes[item.role]?.name ?? item.role}
        key={item.persistentIdentity}
        text={highlightText(item.title, query)}
        active={modifiers.active}
        disabled={modifiers.disabled}
        onClick={handleClick}
      />
    ),
    []
  );
  const onItemSelect = React.useCallback((item: ComponentDefinition, _e) => setSelected(item), []);

  return (
    <>
      <H2>Find parts</H2>
      <Suggest
        fill
        query={rawQuery}
        onQueryChange={onRawQueryChange}
        inputValueRenderer={inputValueRenderer}
        itemRenderer={itemRenderer}
        items={loading ? [] : data ?? []}
        onItemSelect={onItemSelect}
        selectedItem={selected}
        noResults={
          <NonIdealState
            icon={loading ? IconNames.DOWNLOAD : IconNames.SEARCH}
            title={loading ? "Loading results" : "No search results"}
            description={loading ? "Please wait a moment while loading data." : "Your search didn't match any parts."}
          />
        }
        popoverProps={{ minimal: true }}
      />
      {selected && (
        // eslint-disable-next-line @blueprintjs/classes-constants
        <div className="igem-ptop-medium">
          <DraggablePart data={selected} />
          <HTMLTable condensed striped className="igem-mt-small igem-full-width">
            <tbody>
              <tr>
                <td>
                  <strong>Name</strong>
                </td>
                <td>
                  {selected.title}{" "}
                  {selected.title !== selected.displayId && (
                    <span className={Classes.TEXT_MUTED}>({selected.displayId})</span>
                  )}
                </td>
              </tr>
              <tr>
                <td>
                  <strong>Role</strong>
                </td>
                <td>{selected.role}</td>
              </tr>
              <tr>
                <td>
                  <strong>Creator</strong>
                </td>
                <td>{selected.creator}</td>
              </tr>
              <tr>
                <td>
                  <strong>Description</strong>
                </td>
                <td>
                  {selected.description}
                  {selected.description && <br />}
                  {selected.mutableDescription}
                </td>
              </tr>
              <tr>
                <td>
                  <strong>Provenance</strong>
                </td>
                <td>{selected.mutableProvenance}</td>
              </tr>
              <tr>
                <td>
                  <strong>Notes</strong>
                </td>
                <td>{selected.mutableNotes}</td>
              </tr>
              <tr>
                <td />
                <td>
                  <AnchorButton
                    href={selected.persistentIdentity}
                    rightIcon="share"
                    target="_blank"
                    text="View in database"
                  />
                </td>
              </tr>
            </tbody>
          </HTMLTable>
        </div>
      )}
    </>
  );
};

export default Search;
