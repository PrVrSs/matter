# Generated from http.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .httpParser import httpParser
else:
    from httpParser import httpParser

# This class defines a complete generic visitor for a parse tree produced by httpParser.

class httpVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by httpParser#http_message.
    def visitHttp_message(self, ctx:httpParser.Http_messageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#start_line.
    def visitStart_line(self, ctx:httpParser.Start_lineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#request_line.
    def visitRequest_line(self, ctx:httpParser.Request_lineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#method.
    def visitMethod(self, ctx:httpParser.MethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#request_target.
    def visitRequest_target(self, ctx:httpParser.Request_targetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#origin_form.
    def visitOrigin_form(self, ctx:httpParser.Origin_formContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#absolute_path.
    def visitAbsolute_path(self, ctx:httpParser.Absolute_pathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#segment.
    def visitSegment(self, ctx:httpParser.SegmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#query.
    def visitQuery(self, ctx:httpParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#http_version.
    def visitHttp_version(self, ctx:httpParser.Http_versionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#http_name.
    def visitHttp_name(self, ctx:httpParser.Http_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#header_field.
    def visitHeader_field(self, ctx:httpParser.Header_fieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#field_name.
    def visitField_name(self, ctx:httpParser.Field_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#token.
    def visitToken(self, ctx:httpParser.TokenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#field_value.
    def visitField_value(self, ctx:httpParser.Field_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#field_content.
    def visitField_content(self, ctx:httpParser.Field_contentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#field_vchar.
    def visitField_vchar(self, ctx:httpParser.Field_vcharContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#obs_text.
    def visitObs_text(self, ctx:httpParser.Obs_textContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#obs_fold.
    def visitObs_fold(self, ctx:httpParser.Obs_foldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#pchar.
    def visitPchar(self, ctx:httpParser.PcharContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#unreserved.
    def visitUnreserved(self, ctx:httpParser.UnreservedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#sub_delims.
    def visitSub_delims(self, ctx:httpParser.Sub_delimsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#tchar.
    def visitTchar(self, ctx:httpParser.TcharContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by httpParser#vCHAR.
    def visitVCHAR(self, ctx:httpParser.VCHARContext):
        return self.visitChildren(ctx)



del httpParser